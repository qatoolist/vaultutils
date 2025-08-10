#!/usr/bin/env python3
"""Release utility for vaultutils.

This script creates a date-based version tag and pushes it to the repository.
Versions follow the scheme ``v<dd.mm.yy>.<n>`` where ``n`` is the incrementing
release number for that day. A separate GitHub workflow builds the project and
uploads it to PyPI whenever such a tag is pushed.
"""

from __future__ import annotations

import datetime as _dt
import logging
import re
import subprocess
from pathlib import Path

TAG_PATTERN = r"^v\d{2}\.\d{2}\.\d{2}\.\d+$"
VERSION_FILE = Path("src/vaultutils/__about__.py")


def compute_tag() -> tuple[str, str]:
    today = _dt.datetime.now(tz=_dt.UTC).date()
    date_str = today.strftime("%d.%m.%y")
    prefix = f"v{date_str}."

    tags = subprocess.check_output(["git", "tag"], text=True).splitlines()
    pattern = re.compile(rf"^{re.escape(prefix)}(\d+)$")
    numbers = [int(m.group(1)) for t in tags if (m := pattern.match(t))]
    next_num = max(numbers, default=0) + 1
    tag = f"{prefix}{next_num}"
    version = f"{date_str}.{next_num}"
    return tag, version


def write_version(version: str) -> None:
    VERSION_FILE.write_text(f'__version__ = "{version}"\n')


def run(*cmd: str) -> None:
    subprocess.check_call(cmd)


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    tag, version = compute_tag()
    logging.info("Releasing %s as %s", version, tag)
    write_version(version)
    run("git", "commit", "-am", f"chore: release {tag}")
    run("git", "tag", tag)
    run("git", "push", "origin", "HEAD", tag)


if __name__ == "__main__":
    main()
