#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "telegramify-markdown",
# ]
# ///

"""Convert standard markdown to Telegram MarkdownV2."""

import argparse
import sys
from pathlib import Path


def convert_markdown(text: str) -> str:
    """Convert standard markdown to Telegram MarkdownV2."""
    from telegramify_markdown import markdownify
    return markdownify(text, normalize_whitespace=False)


def read_input(args: argparse.Namespace) -> str:
    """Read markdown input from various sources."""
    # 1. Command line argument (positional) - check if it's a file path
    if args.markdown:
        text = args.markdown
        if text.startswith('@'):
            return Path(text[1:]).read_text()
        return text

    # 2. File path (with @ or direct path)
    if args.file:
        path = args.file
        if path.startswith('@'):
            return Path(path[1:]).read_text()
        return Path(path).read_text()

    # 3. stdin - check if there's data piped or redirected
    if not sys.stdin.isatty():
        return sys.stdin.read()

    # No input provided
    return ""


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert standard markdown to Telegram MarkdownV2",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Input sources (mutually exclusive):
  1. positional argument: ./telegram-markdown.py "markdown text"
  2. file path (with @): ./telegram-markdown.py @path/to/file
  3. here-string: ./telegram-markdown.py <<< "markdown"
  4. file redirection: ./telegram-markdown.py < file.txt
  5. pipe: echo "markdown" | ./telegram-markdown.py"""
    )
    parser.add_argument(
        "markdown",
        nargs="?",
        help="Markdown text to convert"
    )
    parser.add_argument(
        "-f", "--file",
        help="Read from file (prefix with @ for curl-style path)"
    )
    args = parser.parse_args()

    # Check for conflicting arguments
    if args.markdown and args.file:
        print("ERROR: Cannot use both positional argument and --file", file=sys.stderr)
        sys.exit(1)

    input_text = read_input(args)

    if not input_text:
        parser.print_help()
        sys.exit(1)

    result = convert_markdown(input_text)
    print(result)


if __name__ == "__main__":
    main()
