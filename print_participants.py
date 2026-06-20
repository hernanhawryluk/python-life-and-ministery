#!/usr/bin/env python3
import sqlite3
import sys

from src.utils.participants_console import fetch_registered_participants


def main():
    try:
        print(fetch_registered_participants())
    except sqlite3.Error as error:
        print(f"No se pudieron obtener los hermanos registrados: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
