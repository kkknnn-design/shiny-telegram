# 每日专辑维护

页面入口为根目录的 `album.html`，可直接打开；安装应用和离线缓存需要 HTTPS 或 localhost。

- `album-additions.tsv`：本次新增专辑和原创听赏笔记。没有核实的第三方评分留空。
- `sync-album-covers.cjs`：核对艺术家和专辑名，下载封面并更新页面内嵌曲库。运行 `node tools/sync-album-covers.cjs`。
- `album-cover-overrides.json`：自动搜索无法解析时使用的已核对专辑页面。
- `../album-assets/cover-sources.json`：每张封面的来源、匹配结果和核对日期。
- `album-catalog.json`：最近一次同步后的完整数据快照。
- `album-style.css`、`album-body.html`、`album-app.js`：界面源文件。修改后运行 `tools/redesign-album.py`，将它们内嵌进 `album.html`。该脚本需要 Pillow，并生成白色唱片图标的 SVG 与 PNG。

验证：`node tests/album.test.cjs`；`tools/check-album-artwork.py` 检查所有图片可解码。浏览器检查脚本 `check-album-browser.js` 应在 `http://127.0.0.1:8787/shiny-telegram/album.html` 执行，用于验证 Pages 子路径下的安装资源与缓存。可用 `node tools/preview-album.cjs` 启动这个预览。

发布时需同时上传 `album.html`、`album-assets/`、`album.webmanifest` 和 `album-sw.js`。更新资源后递增 `album-sw.js` 的缓存版本，帮助已安装应用获取新资源。离线状态下可访问之前缓存的页面和封面，未浏览的封面需要联网加载一次。
