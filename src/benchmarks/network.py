import subprocess

from .base import Benchmark


class NetworkBenchmark(Benchmark):
    def run(self):
        self.logger.header("NETWORK BENCHMARK")
        self.logger.info("Running Speedtest (Ookla)... please wait.")

        try:
            cmd = ["speedtest-cli", "--simple"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    self.logger.info(f"  {line}")
                self.logger.info(f">> Context : High Upload/Download is Good. Low Ping is Good.")
            else:
                self.logger.error(f"‼️ ERROR: Speedtest failed - {result.stderr}")

        except subprocess.TimeoutExpired:
            self.logger.error("‼️ ERROR: Network test timed out.")
        except Exception as e:
            self.logger.excep(f"‼️ ERROR: Network test failed - {str(e)}")
