#!/usr/bin/env python3
"""Build and verify the versioned Syfo landing-page artifact.

The deployable surface is intentionally narrower than ``site/``: generated
root HTML files plus the five locale trees and shared assets. Generator source,
translation inputs, and local notes never enter the production artifact.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import subprocess
import tarfile
from pathlib import Path, PurePosixPath


SCHEMA_VERSION = 1
PUBLIC_DIRECTORIES = ("assets", "en", "es", "ja", "vi", "zh")
PUBLIC_ROOT_SUFFIXES = (".html", ".ico", ".txt", ".webmanifest", ".xml")
MANIFEST_PATH = PurePosixPath("_syfo/landing-manifest.json")
CHECKSUMS_PATH = PurePosixPath("_syfo/SHA256SUMS")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def source_commit(root: Path, override: str | None) -> str:
    if override:
        return override
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=root, text=True
    ).strip()


def collect_files(site: Path) -> list[tuple[PurePosixPath, bytes]]:
    selected: list[Path] = sorted(
        path
        for path in site.iterdir()
        if path.is_file() and path.suffix in PUBLIC_ROOT_SUFFIXES
    )
    for directory in PUBLIC_DIRECTORIES:
        root = site / directory
        if not root.is_dir():
            raise SystemExit(f"landing artifact: missing public directory: {root}")
        selected.extend(sorted(path for path in root.rglob("*") if path.is_file()))

    files: list[tuple[PurePosixPath, bytes]] = []
    seen: set[PurePosixPath] = set()
    for path in selected:
        relative = PurePosixPath(path.relative_to(site).as_posix())
        if relative in seen:
            continue
        seen.add(relative)
        files.append((relative, path.read_bytes()))
    return sorted(files, key=lambda item: item[0].as_posix())


def make_manifest(files: list[tuple[PurePosixPath, bytes]], commit: str) -> dict:
    entries = [
        {"path": path.as_posix(), "sha256": sha256(data), "size": len(data)}
        for path, data in sorted(files, key=lambda item: item[0].as_posix())
    ]
    digest_input = "".join(
        f"{entry['sha256']}  {entry['path']}\n" for entry in entries
    ).encode()
    return {
        "schemaVersion": SCHEMA_VERSION,
        "sourceCommit": commit,
        "contentSha256": sha256(digest_input),
        "files": entries,
    }


def manifest_bytes(manifest: dict) -> bytes:
    return (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode()


def checksums_bytes(manifest: dict) -> bytes:
    return "".join(
        f"{entry['sha256']}  {entry['path']}\n" for entry in manifest["files"]
    ).encode()


def add_bytes(tar: tarfile.TarFile, path: PurePosixPath, data: bytes) -> None:
    info = tarfile.TarInfo(path.as_posix())
    info.size = len(data)
    info.mode = 0o644
    info.mtime = 0
    info.uid = 0
    info.gid = 0
    info.uname = ""
    info.gname = ""
    tar.addfile(info, io.BytesIO(data))


def write_artifact(output: Path, files: list[tuple[PurePosixPath, bytes]], manifest: dict) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, compresslevel=9, mtime=0) as compressed:
            with tarfile.open(fileobj=compressed, mode="w", format=tarfile.PAX_FORMAT) as tar:
                for path, data in sorted(files, key=lambda item: item[0].as_posix()):
                    add_bytes(tar, path, data)
                add_bytes(tar, MANIFEST_PATH, manifest_bytes(manifest))
                add_bytes(tar, CHECKSUMS_PATH, checksums_bytes(manifest))


def read_artifact(artifact: Path) -> tuple[dict, dict[str, bytes]]:
    files: dict[str, bytes] = {}
    with tarfile.open(artifact, "r:gz") as tar:
        for member in tar.getmembers():
            if not member.isfile():
                raise SystemExit(f"landing artifact: non-file entry is forbidden: {member.name}")
            path = PurePosixPath(member.name)
            if path.is_absolute() or ".." in path.parts:
                raise SystemExit(f"landing artifact: unsafe path: {member.name}")
            extracted = tar.extractfile(member)
            if extracted is None:
                raise SystemExit(f"landing artifact: cannot read: {member.name}")
            if member.name in files:
                raise SystemExit(f"landing artifact: duplicate path: {member.name}")
            files[member.name] = extracted.read()
    raw_manifest = files.pop(MANIFEST_PATH.as_posix(), None)
    if raw_manifest is None:
        raise SystemExit("landing artifact: manifest is missing")
    raw_checksums = files.pop(CHECKSUMS_PATH.as_posix(), None)
    if raw_checksums is None:
        raise SystemExit("landing artifact: SHA256SUMS is missing")
    manifest = json.loads(raw_manifest)
    if raw_checksums != checksums_bytes(manifest):
        raise SystemExit("landing artifact: SHA256SUMS does not match manifest")
    return manifest, files


def verify_artifact(artifact: Path, expected_commit: str | None = None) -> dict:
    manifest, files = read_artifact(artifact)
    if manifest.get("schemaVersion") != SCHEMA_VERSION:
        raise SystemExit("landing artifact: unsupported manifest schema")
    if expected_commit and manifest.get("sourceCommit") != expected_commit:
        raise SystemExit(
            "landing artifact: source commit mismatch: "
            f"expected {expected_commit}, got {manifest.get('sourceCommit')}"
        )
    expected_entries = manifest.get("files")
    if not isinstance(expected_entries, list):
        raise SystemExit("landing artifact: manifest files must be an array")
    actual_files = sorted(files)
    listed_files = [entry.get("path") for entry in expected_entries]
    if listed_files != actual_files:
        raise SystemExit("landing artifact: manifest/file set mismatch")
    rebuilt = make_manifest(
        [(PurePosixPath(path), files[path]) for path in actual_files],
        str(manifest.get("sourceCommit", "")),
    )
    if rebuilt != manifest:
        raise SystemExit("landing artifact: checksum or content digest mismatch")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", type=Path, default=Path("site"))
    parser.add_argument("--output", type=Path, default=Path("dist/syfo-landing.tar.gz"))
    parser.add_argument("--source-commit")
    parser.add_argument("--verify", type=Path)
    parser.add_argument("--expected-source-commit")
    args = parser.parse_args()

    if args.verify:
        manifest = verify_artifact(args.verify, args.expected_source_commit)
        print(
            "landing artifact: verified "
            f"{len(manifest['files'])} files, content={manifest['contentSha256']}"
        )
        return

    root = Path(__file__).resolve().parents[1]
    site = args.site if args.site.is_absolute() else root / args.site
    output = args.output if args.output.is_absolute() else root / args.output
    files = collect_files(site)
    manifest = make_manifest(files, source_commit(root, args.source_commit))
    write_artifact(output, files, manifest)
    verify_artifact(output, manifest["sourceCommit"])
    output.with_suffix(output.suffix + ".manifest.json").write_bytes(manifest_bytes(manifest))
    print(
        f"landing artifact: wrote {output} ({len(files)} files, "
        f"content={manifest['contentSha256']})"
    )


if __name__ == "__main__":
    main()
