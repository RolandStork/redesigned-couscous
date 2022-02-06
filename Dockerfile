FROM python:3.10.2-slim-bullseye
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN apt-get update && apt-get install -y dumb-init
COPY requirements.txt ./
RUN pip install -r requirements.txt
ENTRYPOINT ["/usr/bin/dumb-init", "--"]
