FROM ubuntu:trusty
RUN apt-get update
# Install dependencies for PPA
RUN apt-get install -y software-properties-common python-software-properties
RUN add-apt-repository ppa:ethereum/ethereum
RUN apt-get install -y libssl-dev python3-pip wget unzip vim
RUN apt-get install -y systemd libpam-systemd git

# tip provided by @MicahZoltu in ethereum/solidity channel on Gitter
# note: py-solc only supports up to 0.4.17 at the moment 
ARG SOLC_VERSION=v0.4.17
RUN wget --quiet --output-document /usr/local/bin/solc https://github.com/ethereum/solidity/releases/download/${SOLC_VERSION}/solc-static-linux \
    && chmod a+x /usr/local/bin/solc

# Copy over requirements
COPY main.py .
COPY README.md .
COPY requirements.txt .

# Install python dependencies
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN pip3 install web3 py-solc populus
# Fix for populus
RUN export LC_ALL=C.UTF-8
RUN export LANG=C.UTF-8

WORKDIR /code