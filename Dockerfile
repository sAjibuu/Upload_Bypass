# Use an official Python runtime as a parent image
FROM python:latest

# Install git, Nano and Vim to clone your repository
RUN apt-get update && apt-get install -y nano vim wget

# Set the working directory
WORKDIR /Upload_Bypass

COPY . /Upload_Bypass

# Install your Python tool dependencies
RUN pip install -r requirements.txt

RUN chmod +x ./upload_bypass.py

# Set environment variables for proxy configuration
ENV http_proxy=http://127.0.0.1:8080
ENV https_proxy=http://127.0.0.1:8080

# Define the command to run your Python tool
ENTRYPOINT ["python3","./upload_bypass.py"]
