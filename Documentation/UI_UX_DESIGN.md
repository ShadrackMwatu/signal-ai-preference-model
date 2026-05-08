# UI And UX Design

Last updated: 2026-05-08

## Design Goals

Signal's UI should feel like a serious intelligence dashboard: clear, dense enough for analysts, privacy-aware, and stable in hosted environments.

## Main Tabs

- Behavioral Signals AI
- Signal CGE Framework
- SML CGE Workbench
- Learning

## Behavioral Signals AI

This tab includes:

- visible Live Trend Intelligence card
- prediction inputs
- demand classification outputs
- confidence and opportunity outputs
- explanation text
- visual intelligence cards

## Live Trend Intelligence UX

The visible feed should:

- appear immediately on page load
- show active trend count
- show moving topical issues
- avoid raw table exposure
- use fallback topics if live API data is unavailable

## Design Constraints

- Do not expose private or individual-level data.
- Keep tables hidden when they are only backend support.
- Avoid replacing working prediction controls.
- Keep Gradio callbacks simple and predictable.

