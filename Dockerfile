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

# Install Node.js for use of testrpc executable
RUN apt-get install --yes curl
# RUN curl --silent --location https://deb.nodesource.com/setup_4.x | sudo bash -
RUN curl -sL https://deb.nodesource.com/setup_6.x | sudo bash -
# RUN add-apt-repository -y ppa:chris-lea/node.js
RUN apt-get install -y nodejs

# Fix npm since not the latest version installed by apt-get
# RUN npm install -g npm

RUN npm install -g ethereumjs-testrpc

RUN mkdir -p db/chaindb;
