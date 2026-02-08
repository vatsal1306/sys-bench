import logging
import os
import sys


class BenchmarkLogger:
    def __init__(self, log_dir="/data"):
        self.log_file = os.path.join(log_dir, "benchmark_report.log")

        # Setup Logger
        self.logger = logging.getLogger("SysBench")
        self.logger.setLevel(logging.INFO)

        # Formatter
        formatter = logging.Formatter('%(message)s')

        # Stream Handler (Stdout)
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

        # File Handler
        try:
            fh = logging.FileHandler(self.log_file, mode='w')
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)
        except PermissionError:
            print(f"⚠️ WARNING: Cannot write to {self.log_file} due to permission error. Logging to console only.")

    def info(self, message):
        self.logger.info(message)

    def excep(self, message):
        self.logger.exception(message)

    def warn(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def header(self, title):
        self.logger.info(f"\n{'=' * 60}")
        self.logger.info(f" {title}")
        self.logger.info(f"{'=' * 60}")
