# Use PyTorch base image (comes with CUDA/cuDNN)
FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies (fio for disk, git/curl if needed)
RUN apt-get update && \
    apt-get install -y fio curl nano && \
    rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Install Python Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ src/
COPY run.sh .

RUN chmod +x run.sh

# Create the data mount point
RUN mkdir -p /data

ENTRYPOINT ["./run.sh"]