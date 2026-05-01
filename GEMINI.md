# Agent Instructions

This repository is a collection of personal tools. Each tool is a standalone script (Bash or Python) with a single, clear responsibility.

## Core Principles

- **One Tool, One Responsibility:** Every script should do exactly one thing and do it well.
- **Languages:** Prefer Bash for simple system tasks and Python for more complex logic.
- **Location:** All tools must be located in the `bin/` directory.
- **Executability:** Ensure all scripts in `bin/` are executable (`chmod +x`).
- **Documentation:** Each tool should have a brief comment at the top explaining its purpose and usage.

## Development Workflow

1.  **Creation:** When asked to create a new tool, place it in `bin/`.
2.  **Naming:** Use descriptive names (e.g., `git-clean-branches`, `optimize-images.py`).
3.  **Refactoring:** If a tool becomes too complex, split it into multiple smaller tools.
