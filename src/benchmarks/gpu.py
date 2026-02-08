import time

import torch

from .base import Benchmark


class GPUBenchmark(Benchmark):
    def run(self):
        self.logger.header("GPU BENCHMARK")

        if not torch.cuda.is_available():
            self.logger.warn("⚠️ SKIP: No NVIDIA GPU detected or CUDA not available.")
            return

        try:
            device = torch.device("cuda:0")
            props = torch.cuda.get_device_properties(device)
            total_mem_gb = props.total_memory / 1e9

            # Check current usage
            reserved = torch.cuda.memory_reserved(device) / 1e9
            free_mem_gb = total_mem_gb - reserved

            self.logger.info(f"Device     : {props.name}")
            self.logger.info(f"Memory     : {total_mem_gb:.4f} GB Total | {free_mem_gb:.4f} GB Free")

            # Dynamic Scaling
            matrix_size = 14000  # High load
            if free_mem_gb < 2.0:
                self.logger.info("NOTICE: Very Low VRAM (<2GB). Scaling down workload significantly.")
                matrix_size = 2000

            elif free_mem_gb < 4.0:
                self.logger.info("NOTICE: Low VRAM (<4GB). Scaling down workload.")
                matrix_size = 4000

            elif free_mem_gb < 8.0:
                matrix_size = 8000

            iterations = 100  # Loop to stress GPU
            self.logger.info(f"Workload   : ({matrix_size}x{matrix_size}) | Iterations: {iterations}")

            # Allocation
            t1 = torch.randn(matrix_size, matrix_size, device=device)
            t2 = torch.randn(matrix_size, matrix_size, device=device)

            # Warmup
            torch.mm(torch.randn(1024, 1024, device=device), torch.randn(1024, 1024, device=device))
            torch.cuda.synchronize()

            # Benchmark
            start = time.time()
            for _ in range(iterations):
                torch.mm(t1, t2)
            torch.cuda.synchronize()
            end = time.time()

            duration = end - start

            # Formatting Time
            if duration < 1.0:
                time_str = f"{duration * 1000:.4f} ms"
            else:
                time_str = f"{duration} sec"

            total_ops = 2 * (matrix_size ** 3) * iterations
            tflops = total_ops / duration / 1e12  # TeraFLOPS

            self.logger.info(f"Time Taken : {time_str}")
            self.logger.info(f"Score      : {tflops:.2f} TFLOPS (approx)")
            self.logger.info(f"\n>> Context : Higher is Better.")

        except RuntimeError as e:
            if "out of memory" in str(e):
                self.logger.error(f"‼️ ERROR: GPU OOM. The GPU is likely too busy with other tasks. {str(e)}")
            else:
                self.logger.excep(f"‼️ ERROR: GPU Benchmark failed - {str(e)}")
        except Exception as e:
            self.logger.excep(f"‼️ ERROR: Unexpected GPU failure - {str(e)}")
