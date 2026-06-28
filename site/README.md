# Syfo 官网 (marketing site)

中文官网，完全基于本仓库的 **syfo-design** 设计系统（暖纸 surface + 印刷赭石 accent + Noto Serif SC 衬线标题 + Inter 正文 + IBM Plex Mono 标签 + 放射信号 logo）。

面向各行各业的非技术团队，核心讲「人和一群 AI Agent 在同一个工作空间里一起把活干完」，并用真实案例建立可信度。

## 页面

| 页面 | 文件 | 说明 |
|------|------|------|
| 首页 | `index.html` | Hero（真实产品界面截图）+ 两支柱（机制 / 协作）+ 能为你做什么 + 精选案例 + 五步上手 + 多 Agent 接力 |
| 案例列表 | `cases.html` | 6 个跨行业案例卡片（参考 raft.build/resources/use-cases 做法） |
| 案例内页 | `case-*.html` | 每个案例的详情页：行业/起始频道/上手 → 想做什么 → 建频道 → 加 Agent → 房间简报 → 工作流 → 长期任务 → 进阶 → 小贴士 → 相关案例 |
| 怎么用 | `how.html` | Syfo Tour 视频页，按设备自动播放电脑版（横版）或手机版（竖版） |

案例：金融投资·私募基金 / 金融科技·组合管理 / 内容创作·漫画 / 移动产品·vibe coding / 零售·销售与客服 / 新媒体·内容运营。
案例内容均已抽象，不含真实持仓 / 客户名 / 正文 / 敏感经营数字。

## 生成与本地预览

页面由 `build_site.py` 生成（纯 Python，无构建步骤）。改内容只需改脚本顶部的数据（`CASES` / `SCENES` / `STEPS` / `DETAILS` / `HOW_STEPS`）再重新生成：

```bash
cd site
python3 build_site.py          # 生成 index.html / cases.html / how.html / case-*.html
python3 -m http.server 8080    # 本地预览 http://localhost:8080/
```

## 设计 token

`assets/tokens.css` 是从 `prototype/en/syfo/colors_and_type.css` 复制的设计系统 token 源。
Logo（`assets/logo-mark.svg` / `assets/logo-wordmark.svg`）来自设计系统。

## 视频（怎么用页）

`assets/video/SyfoTour-PC.mp4`（1920×1080 横版）与 `SyfoTour-Mobile.mp4`（1080×1920 竖版）是 Syfo Tour 演示视频。
`how.html` 用 `matchMedia(max-width:768px)` + UA 判定，自动给电脑/手机加载对应视频；附封面图 `poster-*.jpg`。

## 部署

静态站，任何静态托管即可。参考部署：Caddy `root * <dir>` + `file_server`，`.mp4` 走默认 `video/mp4` + range（流式播放）。
