
# Fundify: Bank Statement Analysis Tool

## Overview
Fundify offers a comprehensive solution for processing and analyzing bank statements. It combines Python and FastAPI with MQTT messaging for a scalable and efficient financial analysis tool.

## Getting Started

### Prerequisites
Ensure these are installed:
- Docker
- Docker Compose

### GPU Support (Optional)
To leverage GPU power in Docker (if applicable to Fundify):
```bash
# Install NVIDIA Container Toolkit and configure it
curl -fsSL [NVIDIA Toolkit Installation Commands]
sudo systemctl restart docker

# Test GPU integration
docker run --gpus all nvidia/cuda:11.0-base nvidia-smi
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
Your contributions are welcome! Please refer to our Contribution Guidelines.
