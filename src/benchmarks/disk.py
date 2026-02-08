import os
import shutil
import subprocess

from .base import Benchmark


class DiskBenchmark(Benchmark):
    def __init__(self, logger, target_dir="/data"):
        super().__init__(logger)
        self.target_dir = target_dir

    def run(self):
        self.logger.header("DISK I/O BENCHMARK")

        # Check if fio is installed
        if shutil.which("fio") is None:
            self.logger.error("‼️ ERROR: 'fio' tool not found. Skipping disk test.")
            return

        test_file = os.path.join(self.target_dir, "fio_test_file")
        self.logger.info(f"Target Dir : {self.target_dir}")
        self.logger.info(f"Test Type  : Sequential Read/Write (1GB)")

        # Construct FIO command
        # --direct=1 (Bypass OS cache for real disk speed)
        # --rw=read/write
        # --bs=1M (Large block size for throughput test)

        common_args = [
            "fio", "--name=bench", f"--filename={test_file}",
            "--size=1G", "--bs=1M", "--direct=1", "--ioengine=posixaio",
            "--group_reporting", "--terse-version=3", "--output-format=terse"
        ]

        try:
            # 1. WRITE TEST
            self.logger.info("Running Write Test...")
            cmd_write = common_args + ["--rw=write"]
            result = subprocess.run(cmd_write, capture_output=True, text=True)
            if result.returncode == 0:
                # Parse Terse Output (3rd field is bandwidth in KB/s)
                # Format: 3;bench;...;write_kb_sec;...
                parts = result.stdout.split(';')
                write_bw_mb = int(parts[48]) / 1024  # Field 48 is write_bw (approx)
                self.logger.info(f"Write Speed: {write_bw_mb:.2f} MB/s")
            else:
                self.logger.error(f"‼️ Write Test Failed: {result.stderr}")

            # 2. READ TEST
            self.logger.info("Running Read Test...")
            cmd_read = common_args + ["--rw=read"]
            result = subprocess.run(cmd_read, capture_output=True, text=True)
            if result.returncode == 0:
                parts = result.stdout.split(';')
                read_bw_mb = int(parts[7]) / 1024  # Field 7 is read_bw
                self.logger.info(f"Read Speed : {read_bw_mb:.2f} MB/s")
            else:
                self.logger.error(f"‼️ Read Test Failed: {result.stderr}")

            self.logger.info(f">> Context : Higher is Better.")

        except Exception as e:
            self.logger.excep(f"ERROR: Disk Benchmark failed - {str(e)}")
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)

            self.logger.info("Cleaned up test file.")
