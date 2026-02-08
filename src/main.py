import os
import platform
import sys

from benchmarks.cpu import CPUBenchmark
from benchmarks.disk import DiskBenchmark
from benchmarks.gpu import GPUBenchmark
from benchmarks.network import NetworkBenchmark
from utils.logger import BenchmarkLogger


def get_sys_info(logger):
    logger.header("SYSTEM INFO")
    logger.info(f"OS          : {platform.system()} {platform.release()}")
    logger.info(f"Architecture: {platform.machine()}")
    logger.info(f"CPU Cores   : {os.cpu_count()}")


def main():
    # 1. Setup Logging (Log to /data if mounted, else stdout)
    target_dir = sys.argv[1] if len(sys.argv) > 1 else "/data"
    logger = BenchmarkLogger(log_dir=target_dir)

    # 2. System Info
    get_sys_info(logger)

    # 3. Run Benchmarks
    benchmarks = [
        CPUBenchmark(logger),
        GPUBenchmark(logger),
        DiskBenchmark(logger, target_dir=target_dir),
        NetworkBenchmark(logger)
    ]

    for bench in benchmarks:
        bench.run()

    logger.header("BENCHMARK COMPLETE")
    logger.info(f"Report saved to: {os.path.join(target_dir, 'benchmark_report.log')}")


if __name__ == "__main__":
    main()
