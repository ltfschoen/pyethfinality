FROM ubuntu:trusty
RUN apt-get update
# Install dependencies for PPA
RUN apt-get install -y software-properties-common python-software-properties
RUN add-apt-repository ppa:ethereum/ethereum
RUN apt-get install -y tmux python-setuptools
RUN apt-get install -y build-essential automake pkg-config libtool libffi-dev libgmp-dev python3-cffi
RUN apt-get install -y python-dev libssl-dev python3-pip wget unzip vim
RUN apt-get install -y systemd libpam-systemd git

# tip provided by @MicahZoltu in ethereum/solidity channel on Gitter
# note: py-solc only supports up to 0.4.17 at the moment 
ARG SOLC_VERSION=v0.4.17
RUN wget --quiet --output-document /usr/local/bin/solc https://github.com/ethereum/solidity/releases/download/${SOLC_VERSION}/solc-static-linux \
    && chmod a+x /usr/local/bin/solc

# Download Python, extract, configure, compile, test, and install the build
# Reference - https://passingcuriosity.com/2015/installing-python-from-source/
ARG PYTHON_VERSION=3.6.3
RUN wget https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz
# Ignore `make test`
RUN tar xf Python-${PYTHON_VERSION}.tgz && cd Python-${PYTHON_VERSION} && ./configure && make && make install
# Source the bash_profile in linux with `. ~/.bash_profile`
RUN echo 'PATH="$HOME/bin/python3:$PATH"; export PATH' >> ~/.bash_profile && . ~/.bash_profile
# Fixes https://trello.com/c/K6jmmjvo/29-conflicts-due-to-cached-pyc-files
RUN echo 'export PYTHONDONTWRITEBYTECODE=1' >> ~/.bash_profile && . ~/.bash_profile
RUN which python3
RUN which pip3

# Copy over requirements
COPY ./scripts/src/main.py .
COPY ./README.md .
COPY ./requirements.txt .

# Install python dependencies
# RUN pip3 install --upgrade pip

# Avoid errors when running requirements.txt
RUN pip3 install --upgrade cffi
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
