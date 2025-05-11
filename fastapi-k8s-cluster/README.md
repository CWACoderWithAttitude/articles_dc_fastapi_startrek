# FastAPI Kubernetes Cluster

This project sets up a FastAPI application deployed on a Kubernetes cluster using Kind (Kubernetes in Docker). Below are the details for setting up and running the application.

## Project Structure

```
fastapi-k8s-cluster
├── src
│   ├── Dockerfile          # Dockerfile for building the FastAPI application image
│   ├── main.py             # Main entry point for the FastAPI application
│   ├── ship_model.py       # Data models for the FastAPI application
│   ├── settings.py         # Configuration settings for the FastAPI application
│   └── routers
│       └── __init__.py     # Package for organizing API routes
├── k8s
│   ├── deployment.yaml      # Kubernetes deployment configuration
│   ├── service.yaml         # Kubernetes service configuration
│   └── ingress.yaml         # Ingress configuration for external access
├── kind-config.yaml         # Configuration for creating a Kind cluster
├── requirements.in          # List of dependencies for the FastAPI application
├── requirements.txt         # Generated requirements file for pip
└── README.md                # Project documentation
```

## Prerequisites

- Docker installed on your machine
- Kind installed for creating Kubernetes clusters
- kubectl installed for interacting with the Kubernetes cluster

## Setup Instructions

1. **Create the Kind Cluster:**
   Run the following command to create a Kind cluster using the provided configuration:
   ```
   kind create cluster --config kind-config.yaml
   ```

2. **Build the Docker Image:**
   Navigate to the `src` directory and build the Docker image:
   ```
   cd src
   docker build -t fastapi-app .
   ```

3. **Deploy the Application:**
   Apply the Kubernetes configurations to deploy the FastAPI application:
   ```
   kubectl apply -f ../k8s/deployment.yaml
   kubectl apply -f ../k8s/service.yaml
   kubectl apply -f ../k8s/ingress.yaml
   ```

4. **Access the Application:**
   Once the application is deployed, you can access it via the ingress. Check the ingress configuration for the URL or IP address.

## Usage

After setting up the cluster and deploying the application, you can interact with the FastAPI application through the defined API routes. Refer to the `main.py` file for the available endpoints.

## Additional Information

For any issues or contributions, please refer to the project's GitHub repository or contact the maintainers.