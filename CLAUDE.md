# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a collection of small standalone applications. Each file is self-contained with no shared dependencies between them.

## Projects

- **`pomodoro.py`** — Desktop Pomodoro timer using tkinter. Requires Python 3.x with tkinter (included in standard Windows Python install). Run with `python pomodoro.py`. Uses `winsound.Beep()` for audio alerts (Windows-only).
- **`minesweeper.html`** — Browser-based Minesweeper game. Open directly in a browser, no server needed.
- **`grapher.html`** — Interactive function graph plotter with property analysis. Open directly in a browser, no server needed. Uses math.js CDN for expression parsing and symbolic differentiation. Supports pan, zoom, and PNG export. Displays domain, range, intercepts, parity, monotonicity, extrema, and asymptotes.
- **`album.html`** — Daily album recommender (Chinese UI), 400 albums embedded in source. Open directly in a browser; PWA install/offline needs HTTPS or localhost. Each album shows its original-release cover (local files in `album-assets/covers/`), genre tags, ratings where recorded, and liner notes: 创作背景 / 聆听赏析 / 推荐曲目, loaded from `album-assets/notes.js`. Page accent colour is sampled from the cover; light/dark theme toggle; search, genre chips, sort, history, `#artist|title` deep links. **Do not hand-edit `album.html`**: UI sources are `tools/album-style.css`, `tools/album-body.html`, `tools/album-app.js` (run `python tools/redesign-album.py` to embed, needs Pillow); notes sources are `tools/album-notes/*.txt` (run `python tools/build-album-notes.py`). Bump the cache name in `album-sw.js` after changing assets. Tests: `node --test tests/album.test.cjs`; preview: `node tools/preview-album.cjs`. See `tools/album-maintenance.md`.

- **`cs-sens.html`** — CS2 mouse sensitivity lab (Chinese UI). Open directly in a browser, no server or CDN needed. Three parts: eDPI / cm-per-360 calculator, a pointer-lock 3D aim range that narrows sensitivity over 4 A/B rounds (uses CS2's `m_yaw 0.022` and 16:9 FOV so in-page sensitivity matches in-game feel; requests `unadjustedMovement` raw input), and a ruler-based DPI check. `window.__simLock` / `window.__sensLab` are test hooks for driving the range without real pointer lock.

## No Build/Tests

There are no build scripts, package manifests, or tests. Each `.py`/`.html` file runs independently with zero external dependencies.
