# **System Benchmark Tool**

A unified, containerized benchmarking suite designed for **Linux** servers. This tool performs stress tests and performance measurements for **CPU**, **GPU (CUDA)**, **Disk I/O**, and **Network speed** in a safe, reproducible environment.

## **🚀 Features**

* **CPU Benchmark:** Performs dense `float32` Matrix Multiplication to calculate **GFLOPS**.  
* **GPU Benchmark (Smart):**  
  * Auto-detects **NVIDIA GPUs**.  
  * **Safety First:** Checks available VRAM before running. If the GPU is busy (e.g., training a model), it scales down the workload to prevent Out-Of-Memory (OOM) crashes.  
  * Measures Compute **TFLOPS** (approx).  
* **Disk Benchmark:**  
  * Uses `fio` for industry-standard accuracy.  
  * Uses `--direct=1` to bypass OS RAM caching for true disk speed.  
  * Tests Sequential Read and Write (1GB).  
* **Network Benchmark:**  
  * Upload/Download/Ping latency using `speedtest-cli`.  
* **Dual Logging:** Results are printed to the console *and* saved to log file `benchmark_report.log`.

## **📋 Prerequisites**

1. **Docker** installed. Check with `docker --version`.  
2. **NVIDIA Container Toolkit** installed (Required for GPU tests to work inside Docker).  
3. **Internet Access** (Required for the Network Speedtest).

## **📂 Project Structure**
```text
sys-bench/  
├── docker-compose.yml    # Docker orchestration file  
├── Dockerfile            # Docker image  
├── run.sh                # Entry point script (wraps Python execution)  
├── requirements.txt      # Python dependencies  
└── src/                  # Source code  
    ├── __init__.py       # Versioning
    ├── main.py  
    └── benchmarks/       # Individual test modules
```

## **⚡ How to Run**

### **Method 1: Pulling from Docker Hub (Recommended)**
The fastest way to run the tool without cloning the source code is to pull from [our docker hub](https://hub.docker.com/r/vatsal1306/sys-bench/tags). If you want to run any previous version, you can specify the tag (e.g., `1.0.0`). The `latest` tag will always point to the most recent build version.

```shell
docker run --rm --gpus all -v $(pwd):/data vatsal1306/sys-bench:latest
````

### **Method 2: Using Docker Compose **

Recommended if you have cloned the repository and want to modify the code. It handles volume mounting and GPU resource flags automatically.

1. **Build and Run Docker:**  
```shell
docker-compose up --build
```

2. **View Results:**  
   * Live output will appear in your terminal.  
   * A report file will be generated in your current directory: `./benchmark_report.log`

### **Method 3: Manual Docker Run**

If you prefer to build the image manually:

1. **Build the Image:**  
```shell
docker build -t sys-bench .
```

2. **Run the Container:**  
   * `-v $(pwd):/data`: Maps your current directory to the container to save logs and test disk speed.  
   * `--gpus all`: Passes NVIDIA GPUs to the container.
```shell
docker run --rm --gpus all -v $(pwd):/data sys-bench
```

## **📊 Interpreting Results**

| Metric | Component | Description | Context |
| :---- | :---- | :---- | :---- |
| **GFLOPS** | CPU | Giga Floating Point Operations Per Second. | **Higher is Better.** Measures raw math speed. |
| **TFLOPS** | GPU | Tera Floating Point Operations Per Second. | **Higher is Better.** Measures CUDA compute throughput. *Note: Score depends on available VRAM.* |
| **MB/s** | Disk | Megabytes per Second. | **Higher is Better.** Speed of writing/reading from physical disk. |
| **Mbps** | Network | Megabits per Second. | **Higher is Better.** Internet connection bandwidth. |

## **⚠️ Troubleshooting**

**1. GPU not detected**

* Ensure you have the NVIDIA drivers installed on the host.  
* Ensure `nvidia-container-toolkit` is installed.  
* Verify the container runtime includes `--gpus all`.

**2. Disk Benchmark Fails or Permissions Error**

* The tool tries to write a temporary file to the mounted volume (`/data` inside container, which is `$(pwd)` on host).  
* Ensure your current directory is writable by the user running Docker.  
* If using Docker Compose, you may need to map the user ID by uncommenting the `user:` line in [docker-compose.yml](docker-compose.yml).

**3\. Network Test Fails**

* Check if the server has outbound internet access.  
* Some corporate firewalls could block speedtest endpoints.

## **📈 Future Enhancements**
* Add support for AMD GPUs and Metal (macOS).

## **📜 License**
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## **📞 Contact**
For questions or support, please open an issue on GitHub or contact the maintainer at [