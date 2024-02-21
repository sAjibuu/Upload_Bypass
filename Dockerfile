FROM python:latest
RUN apt-get update && apt-get install -y nano vim wget
WORKDIR /opt
COPY . /opt/upload_bypass
WORKDIR /opt/upload_bypass
RUN python3 -m pip install -r requirements.txt
ENTRYPOINT ["python3","upload_bypass.py"]
