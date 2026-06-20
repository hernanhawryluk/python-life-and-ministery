#!/usr/bin/env python3
import argparse
import datetime
import itertools
import sys
import threading

from src.utils.meeting_program_console import fetch_next_month_program


class ConsoleLoader:
    def __init__(self, message="Consultando el programa en WOL", stream=None, interval=0.1):
        self.message = message
        self.stream = stream or sys.stderr
        self.interval = interval
        self.stop_event = threading.Event()
        self.thread = None

    def __enter__(self):
        if not self.stream.isatty():
            self.stream.write(f"{self.message}...\n")
            self.stream.flush()
            return self

        self.thread = threading.Thread(target=self._animate, daemon=True)
        self.thread.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop_event.set()
        if self.thread:
            self.thread.join()
            self.stream.write("\r\033[K")
            self.stream.flush()

    def _animate(self):
        for frame in itertools.cycle("|/-\\"):
            if self.stop_event.is_set():
                break
            self.stream.write(f"\r{self.message}... {frame}")
            self.stream.flush()
            self.stop_event.wait(self.interval)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Muestra el programa de Vida y Ministerio del próximo mes.",
    )
    parser.add_argument(
        "--date",
        type=datetime.date.fromisoformat,
        help="Fecha de referencia YYYY-MM-DD (opcional; por defecto usa hoy).",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=20,
        help="Tiempo máximo por consulta a WOL en segundos (por defecto: 20).",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    try:
        with ConsoleLoader():
            program = fetch_next_month_program(args.date, args.timeout)
        print(program)
    except (RuntimeError, ValueError) as error:
        print(f"No se pudo obtener el programa: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
