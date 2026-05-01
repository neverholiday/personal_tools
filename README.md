# Personal Tools

A collection of modular, single-responsibility scripts for personal productivity and system automation.

## Philosophy

This repository follows a strict "One Tool, One Responsibility" philosophy. Every script is designed to do exactly one thing efficiently.

- **Modular:** Each tool is a standalone script.
- **Predictable:** Scripts are either Bash (for system tasks) or Python (for logic-heavy tasks).
- **Accessible:** All tools are located in the `bin/` directory.

## Getting Started

1.  **Explore:** Check the `bin/` directory for available tools.
2.  **Use:** Add the `bin/` directory to your `PATH` to use the tools from anywhere:
    ```bash
    export PATH="$PATH:$(pwd)/bin"
    ```
3.  **Learn:** Read the comments at the top of each script to understand its specific usage.

## Development

For detailed instructions on how to contribute or create new tools, see [GEMINI.md](./GEMINI.md).
