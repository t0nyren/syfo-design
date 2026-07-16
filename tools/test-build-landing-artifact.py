#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import json
import tarfile
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("build-landing-artifact.py")
SPEC = importlib.util.spec_from_file_location("landing_artifact", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class LandingArtifactTest(unittest.TestCase):
    def fixture(self, root: Path) -> Path:
        site = root / "site"
        for directory in MODULE.PUBLIC_DIRECTORIES:
            (site / directory).mkdir(parents=True)
            (site / directory / "index.html").write_text(directory, encoding="utf-8")
        (site / "index.html").write_text("root", encoding="utf-8")
        (site / "robots.txt").write_text("User-agent: *", encoding="utf-8")
        (site / "sitemap.xml").write_text("<urlset/>", encoding="utf-8")
        (site / "build_site.py").write_text("secret", encoding="utf-8")
        (site / "i18n").mkdir()
        (site / "i18n" / "en.json").write_text("{}", encoding="utf-8")
        return site

    def test_public_allowlist_and_verification(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            files = MODULE.collect_files(self.fixture(root))
            names = [path.as_posix() for path, _ in files]
            self.assertIn("index.html", names)
            self.assertIn("robots.txt", names)
            self.assertIn("sitemap.xml", names)
            self.assertIn("en/index.html", names)
            self.assertNotIn("build_site.py", names)
            self.assertNotIn("i18n/en.json", names)

            manifest = MODULE.make_manifest(files, "a" * 40)
            artifact = root / "landing.tar.gz"
            MODULE.write_artifact(artifact, files, manifest)
            self.assertEqual(MODULE.verify_artifact(artifact, "a" * 40), manifest)

    def test_tampered_payload_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            files = MODULE.collect_files(self.fixture(root))
            manifest = MODULE.make_manifest(files, "b" * 40)
            artifact = root / "landing.tar.gz"
            MODULE.write_artifact(artifact, files, manifest)

            replacement = root / "tampered.tar.gz"
            with tarfile.open(artifact, "r:gz") as source, tarfile.open(replacement, "w:gz") as target:
                for member in source.getmembers():
                    extracted = source.extractfile(member)
                    assert extracted is not None
                    data = extracted.read()
                    if member.name == "index.html":
                        data = b"tampered"
                        member.size = len(data)
                    import io

                    target.addfile(member, io.BytesIO(data))
            with self.assertRaises(SystemExit):
                MODULE.verify_artifact(replacement, "b" * 40)

    def test_manifest_is_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            files = MODULE.collect_files(self.fixture(root))
            first = MODULE.make_manifest(files, "c" * 40)
            second = MODULE.make_manifest(list(reversed(files)), "c" * 40)
            self.assertEqual(json.dumps(first, sort_keys=True), json.dumps(second, sort_keys=True))
            first_artifact = root / "first.tar.gz"
            second_artifact = root / "second.tar.gz"
            MODULE.write_artifact(first_artifact, files, first)
            MODULE.write_artifact(second_artifact, list(reversed(files)), second)
            self.assertEqual(first_artifact.read_bytes(), second_artifact.read_bytes())


if __name__ == "__main__":
    unittest.main()
