import time

import torch

from .base import Benchmark


class CPUBenchmark(Benchmark):
    def run(self):
        self.logger.header("CPU BENCHMARK")

        matrix_size = 4000
        self.logger.info(f"Test: Dense Matrix Multiplication (Float32)")
        self.logger.info(f"Size: {matrix_size}x{matrix_size}")

        try:
            # Generate random matrices
            t1 = torch.rand(matrix_size, matrix_size)
            t2 = torch.rand(matrix_size, matrix_size)

            start_time = time.time()
            torch.mm(t1, t2)
            end_time = time.time()

            duration = end_time - start_time
            # Calculate GFLOPS: 2 * N^3 operations
            gflops = (2 * (matrix_size ** 3)) / duration / 1e9

            self.logger.info(f"Time Taken : {duration:.4f} seconds")
            self.logger.info(f"Score      : {gflops:.2f} GFLOPS")
            self.logger.info(f">> Context : Higher is Better.")

        except Exception as e:
            self.logger.excep(f"ERROR: CPU Benchmark failed - {str(e)}.")
