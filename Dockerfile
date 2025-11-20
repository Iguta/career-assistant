# Use Python 3.13 (or 3.12) as base image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the setup script and apply uvicorn patch
# The patch is needed for nest_asyncio compatibility with Python 3.12+
COPY setup_uvicorn_patch.py .
RUN python setup_uvicorn_patch.py

# Copy project files
COPY . .

# Create directory for Jupyter runtime files
RUN mkdir -p /root/.jupyter

# Expose ports
# 7860 for Gradio, 8888 for Jupyter
EXPOSE 7860 8888

# Set environment variables for Jupyter
ENV JUPYTER_ENABLE_LAB=yes
ENV PYTHONUNBUFFERED=1

# Default command: start Jupyter Lab
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=''", "--NotebookApp.password=''"]

