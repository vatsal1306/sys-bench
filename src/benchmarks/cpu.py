import time

import torch

from .base import Benchmark


class CPUBenchmark(Benchmark):
    def run(self):
        self.logger.header("CPU BENCHMARK")

        matrix_size = 4000
        iterations = 30  # Run n times to increase duration

        self.logger.info(f"Test: Dense Matrix Multiplication (Float32)")
        self.logger.info(f"Matrix size: {matrix_size}x{matrix_size} | Iterations: {iterations}")

        try:
            # Generate random matrices
            t1 = torch.rand(matrix_size, matrix_size)
            t2 = torch.rand(matrix_size, matrix_size)

            start_time = time.time()

            # Loop for stress test
            for _ in range(iterations):
                torch.mm(t1, t2)

            end_time = time.time()
            duration = end_time - start_time

            # Formatting Time
            if duration < 1.0:
                time_str = f"{duration * 1000} ms"
            else:
                time_str = f"{duration} seconds"

            # Calculate GFLOPS: (2 * N^3 * iterations) operations
            total_ops = 2 * (matrix_size ** 3) * iterations
            gflops = total_ops / duration / 1e9

            self.logger.info(f"Time Taken : {time_str}")
            self.logger.info(f"Score      : {gflops:.4f} GFLOPS")
            self.logger.info(f"\n>> Context : Higher is Better.")

        except Exception as e:
            self.logger.excep(f"‼️ ERROR: CPU Benchmark failed - {str(e)}")
