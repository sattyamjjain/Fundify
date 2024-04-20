
# Fundify: Bank Statement Analysis Tool

## Overview

Fundify is a state-of-the-art tool designed for processing and analyzing bank statements efficiently. Utilizing a combination of Python and FastAPI, integrated with MQTT messaging, it ensures scalable and reliable financial analysis.

## Compatibility

Tested and verified on multiple platforms to ensure robust performance across diverse environments:

- **llama2**
- **gemma**
- **llama3**
- Additional platforms as required

## Getting Started

### Prerequisites

Before installation, ensure the following are installed:
- Docker
- Docker Compose

### GPU Support (Optional)
To leverage GPU power in Docker (if applicable to Fundify):
```bash
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
  && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit

# Configure NVIDIA Container Toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker

# Test GPU integration
docker run --gpus all nvidia/cuda:11.5.2-base-ubuntu20.04 nvidia-smi
```

### Installation
Clone Fundify Repository:
```bash
git clone https://github.com/sattyamjjain/Fundify.git
cd Fundify
```

Install Dependencies:
```bash
pip install -r requirements.txt
```

### Docker Deployment
```bash
docker-compose up --build
```

## Usage

### Uploading Bank Statements
- **Endpoint**: `/api/upload-statement/`
- **Method**: POST
- **Example**:
  ```bash
  curl -X POST "http://localhost:8000/api/upload-statement/" 
  -H "accept: application/json" 
  -F "bank_name=YourBankName" 
  -F "file=@/path/to/file"
  ```

## System Architecture
- **FastAPI**: Robust API development.
- **MQTT**: Scalable messaging.
- **Pandas**: Data manipulation and analysis.
- **Docker**: Simplified deployment and environment management.

## Stopping and Cleaning Up
```bash
docker-compose down
```

## Contributing

Encourage contributions by guiding users on how to contribute. For example:

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a pull request.
