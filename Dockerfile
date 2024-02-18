FROM python:3.8-alpine
WORKDIR /opt
COPY . /opt/upload_bypass
WORKDIR /opt/upload_bypass
RUN apk add gcc musl-dev
RUN python3 -m pip install -r requirements.txt
ENTRYPOINT ["python3","upload_bypass.py"]
