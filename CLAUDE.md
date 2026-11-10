# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a collection of small standalone applications. Each file is self-contained with no shared dependencies between them.

## Projects

- **`pomodoro.py`** — Desktop Pomodoro timer using tkinter. Requires Python 3.x with tkinter (included in standard Windows Python install). Run with `python pomodoro.py`. Uses `winsound.Beep()` for audio alerts (Windows-only).
- **`minesweeper.html`** — Browser-based Minesweeper game. Open directly in a browser, no server needed.
- **`grapher.html`** — Interactive function graph plotter with property analysis. Open directly in a browser, no server needed. Uses math.js CDN for expression parsing and symbolic differentiation. Supports pan, zoom, and PNG export. Displays domain, range, intercepts, parity, monotonicity, extrema, and asymptotes.
- **`album.html`** — Daily album recommender drawing from Pitchfork, RateYourMusic, and Rolling Stone charts. Open directly in a browser, no server needed. Recommends one album per day with cover art, genre tags, ratings from all three sources, and artist biography. Supports skipping to a random different album and browsing history.
- **`cs-sens.html`** — CS2 mouse sensitivity lab (Chinese UI). Open directly in a browser, no server or CDN needed. Three parts: eDPI / cm-per-360 calculator, a pointer-lock 3D aim range that narrows sensitivity over 4 A/B rounds (uses CS2's `m_yaw 0.022` and 16:9 FOV so in-page sensitivity matches in-game feel; requests `unadjustedMovement` raw input), and a ruler-based DPI check. `window.__simLock` / `window.__sensLab` are test hooks for driving the range without real pointer lock.

## No Build/Tests

There are no build scripts, package manifests, or tests. Each `.py`/`.html` file runs independently with zero external dependencies.
