from .base import Benchmark
from .cpu import CPUBenchmark
from .disk import DiskBenchmark
from .gpu import GPUBenchmark
from .network import NetworkBenchmark

# Explicitly define what is exported when someone uses "from benchmarks import *"
__all__ = [
    "Benchmark",
    "CPUBenchmark",
    "GPUBenchmark",
    "DiskBenchmark",
    "NetworkBenchmark"
]
