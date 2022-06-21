FROM python:3.8

# install build utilities
RUN apt-get update && \
	apt-get install -y gcc make apt-transport-https ca-certificates build-essential

# check our python environment
RUN python3 --version
RUN pip3 --version

# set the working directory for containers
WORKDIR  /usr/src/bitcoin-predictor

# Installing python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all the files from the project’s root to the working directory
COPY src/ /src/
COPY model/ /model/

RUN ls -la /src/*
RUN ls -la /model/*

EXPOSE 5000

CMD ["python3", "/src/app.py"]