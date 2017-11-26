# README

---
PyEthFinality
---

* Trello Board (Project Planning) - https://trello.com/b/rkTmcLNw/pyethfinality

# Table of Contents
  * [Chapter 0 - Quick Start Guide](#chapter-0)
  * [Chapter 1 - Docker Setup](#chapter-1)
  * [Chapter 2 - Tests](#chapter-2)
  * [Chapter 3 - Editor / IDE](#chapter-3)
  * [Chapter 100 - Contributors, Bugs & Issues](#chapter-100)
  * [Chapter 999 - Unsorted](#chapter-999)
  * [Chapter 1000 - ERRORS - macOS Unix Bash Setup Attempt](#chapter-1000)

## Chapter 0 - Quick Start Guide <a id="chapter-0"></a>

* Clone https://github.com/ltfschoen/pyethfinality
* Install and run Docker for Mac
* Run `docker-compose up --force-recreate --build -d`
* Get the container_id with `docker ps -l`
* Create 1st Bash Terminal tab and run interactive Docker shell (for running Python script) with `docker exec -it <container_id> bash`
* Create 2nd Bash Terminal tab and run interactive Docker shell (for TestRPC) with `docker exec -it <container_id> bash`
* Create 3rd Bash Terminal tab and run interactive Docker shell (for cURL requests to API) with `docker exec -it <container_id> bash`
* Start up the TestRPC in the 2nd Bash Terminal's Docker shell
  ```
  rm -rf ./db;
  mkdir -p db/chaindb;
  testrpc --account '0x0000000000000000000000000000000000000000000000000000000000000001, 10002471238800000000000' \
    --account '0x0000000000000000000000000000000000000000000000000000000000000002, 10004471238800000000000' \
    --unlock '0x0000000000000000000000000000000000000000000000000000000000000001' \
    --unlock '0x0000000000000000000000000000000000000000000000000000000000000002' \
    --blocktime 0 \
    --deterministic true \
    --port 8545 \
    --hostname localhost \
    --gasPrice 20000000000 \
    --gasLimit 0x47E7C4 \
    --debug true \
    --mem true \
    --db './db/chaindb'
  ```
* Run the Python script in the 1st Bash Terminal tab's Docker shell 
  ```
  python3 ./scripts/src/main.py
  ```
* Run cURL request to simulate request to API from a front-end Client App in the 3rd Bash Terminal tab's Docker shell
  ```
  curl -i 127.0.0.1:5000/api/v1.0/query?query=None&median_balance=True
  ```
  * Screenshot of response containing median account balance

    ![alt tag](https://raw.githubusercontent.com/ltfschoen/pyethfinality/master/screenshots/api_response_middleware.png)

* Run PyTest in Docker shell
  ```
  python3 -m pytest .
  ```

## Chapter 1 - Docker Setup <a id="chapter-1"></a>

* Docker
  * Run Docker for Mac
  * Run Docker Container / Remove existing Docker network from image. Use Ubuntu packages listed at: https://packages.ubuntu.com/search?suite=all&section=all&arch=any&keywords=solc&searchon=names
    ```
    docker-compose down
    docker-compose up --force-recreate --build -d
    ```
  * Open Docker sandbox session (Multiple tabs)
    ```
    docker ps -l
    
    # run interactive shell to the container 
    docker exec -it <container_id> bash
    
    # create other interaction shells to the container (to run TestRPC)
    docker exec -it <container_id> bash
    ```
  * Open Docker sandbox session (Single tab)
    ```
    docker-compose exec sandbox bash
    ```
    * Show Linux version - http://docs.python-guide.org/en/latest/starting/install3/linux/
      ```
      cat /proc/version
      python3 --version
      solc --help

      export LC_ALL=C.UTF-8
      export LANG=C.UTF-8
      populus
      ```
      * TODO - Add PyEnv and switch to latest version of Python 3

  * Run (Docker terminal tab 2)
    ```
    rm -rf ./db;
    mkdir -p db/chaindb;
    testrpc --account '0x0000000000000000000000000000000000000000000000000000000000000001, 10002471238800000000000' \
      --account '0x0000000000000000000000000000000000000000000000000000000000000002, 10004471238800000000000' \
      --unlock '0x0000000000000000000000000000000000000000000000000000000000000001' \
      --unlock '0x0000000000000000000000000000000000000000000000000000000000000002' \
      --blocktime 0 \
      --deterministic true \
      --port 8545 \
      --hostname localhost \
      --gasPrice 20000000000 \
      --gasLimit 0x47E7C4 \
      --debug true \
      --mem true \
      --db './db/chaindb'
    ```

  * Run (Docker terminal tab 1)
    ```
    python3 ./scripts/src/main.py
    ```
  * Other
    * Show where Python Packages are installed
      ```
      python3 -m site
      which /root/.py-solc/solc-v0.4.17/bin/solc
      python3 -m solc.install v0.4.17
      ```
    * Note: Any files created or modified in the /code directory of the Docker VM are synchronised with this project
    * Note: Manually compile Solidity smart contract with `solc --bin -o $PWD/solcoutput dapp-bin=/usr/local/lib/dapp-bin contract.sol`

  * Other Docker commands not necessary
    ```
    docker network ps
    docker network rm pyethfinality_default
    ```
    * References:
      * https://docs.docker.com/compose/reference/up/
      * https://docs.docker.com/engine/reference/commandline/network_prune/#related-commands

  * IGNORE - Unsuccessful attempt to install Solc using Snap on Ubuntu 16.04 (or Snapd on Ubuntu 14.04).
    * Snapcraft - https://docs.snapcraft.io/core/install-ubuntu
    * Snapd - https://github.com/snapcore/snapd
    * Snapd - https://wiki.archlinux.org/index.php/Snapd
    * Systemd - https://wiki.ubuntu.com/systemd
    * Forum - https://forum.snapcraft.io/c/snapd
    ```
    apt-get install snapd
    snap --help
    ls /lib/systemd/system/snap*; echo; systemctl list-unit-files | grep snap; echo; dpkg -L snapd | grep systemd; echo; pgrep -a snap
    ```
    * Note: The following approach to try and install Solc did not work as I encountered the error `Failed to get D-Bus connection: No connection to service manager.` and could not overcome it. 
      ```
      snap download solc
      systemctl status snapd.service
      systemctl enable snapd
      service snap start
      /usr/lib/snapd/snapd
      ```
    * Check if booting with Systemd
      ```
      ps -p 1 -o comm=
      ```
    * Attempt to boot with Systemd by changing the docker-compose.yml file with the following instead of `command: tail -f /dev/null` did not work either
      ```
      command: /lib/systemd/systemd
      ```
    * After trying all the steps in this section without success, I asked a question on ethereum/solidity channel of Gitter. I received a response from @MicahZoltu, who suggested adding the following to my Dockerfile, which worked. I was then able to run `solc --help` in the Docker VM.
      ```
      ARG SOLC_VERSION=v0.4.18
      RUN wget --quiet --output-document /usr/local/bin/solc https://github.com/ethereum/solidity/releases/download/${SOLC_VERSION}/solc-static-linux \
          && chmod a+x /usr/local/bin/solc
      ```

## Chapter 2 - Tests <a id="chapter-2"></a>

* Run PyTest in Docker shell
  ```
  python3 -m pytest .

  python3 -m pytest tests/
  populus deploy --chain tester --no-wait-for-sync
  ```

## Chapter 3 - Editor / IDE <a id="chapter-3"></a>

* Editor
  * Visual Studio (VS) Code
  * Setup - View Extensions - Press `SHIFT+CMD+X`
    * solidity
    * Solidity Extended
    * solidity-solhint
  * Compile Solidity Contract in VS Code - Press `FN+F5`

  * IntelliJ Debugging with breakpoints in Python
    * `brew install python3`
    * File > Project Structure > Project SDK > New > /Users/Ls/.pyenv/versions/3.6.3/bin/python3
      * Note: Assumes using PyEnv
    * Edit Configurations > Click (+) > Python > Select Project SDK > Ok
    * Allow use of breakpoints (add *.py file type instead of just default *.pyw)
      * Preferences (CMD+,) > Editor > File Types > Add Wildcard > *.py
    * Run > Debug 'mockchain'



## Chapter 100 - Contributors, Bugs & Issues <a id="chapter-100"></a>

* To report an issue, please create a Github issue with the following details:
  * Which version of Solidity you are using
  * What was the source code (if applicable)
  * Which platform are you running on
  * How to reproduce the issue
  * What was the result of the issue
  * What was the expected behaviour

## Chapter 999 - Unsorted <a id="chapter-999"></a>

* Setup Populus Framework - http://populus.readthedocs.io/en/latest/quickstart.html#debian-ubuntu-mint
  * Install Populus
    ```
    pip3 install populus
    export LC_ALL=C.UTF-8
    export LANG=C.UTF-8
    ```
  * Initialise Populus
    ```
    populus init
    ```
  * Compile contract into ./build directory
    ```
    populus compile
    ```

* TODO - Testing with PyTest  
* TODO - Front-End with Truffle

* Reference 
  * Finality - https://blog.ethereum.org/2016/05/09/on-settlement-finality/
  
* Other References
  * Cloud9 / Linux PyEthereum - https://forum.ethereum.org/discussion/comment/16737#Comment_16737
  * Cloud9 / Linux PyEthereum - http://joeysprogrammingblog.com/tag/pyethereum/

## Chapter 1000 - ERRORS - macOS Unix Bash Setup Attempt <a id="chapter-1000"></a>

Initially the approach was to try to create a Python application on macOS in Unix Bash without a virtual machine. I used the quick start code provided at https://github.com/pipermerriam/web3.py / https://pypi.python.org/pypi/web3/ to write main.py, and setup TestRPC code in a separate terminal window using a code snippet that I had previously prepared for another project (https://github.com/ltfschoen/solidity_test). The intention was to use Py-Solc as a wrapper for Solc.js in order to be able to use the Solidity compiler to compile the sample smart contract that was written in Solidity, but this did not work and I took drastic steps to try and make it work. Web3.py would then deploy it to the TestRPC blockchain. Unfortunately I encountered errors, so I decided to try to use a virtual machine with Docker instead.
If you happen to know how to overcome the error I would be grateful if you would please create an [Issue](https://github.com/ltfschoen/pyethfinality/issues) and explain it.

* Setup PyEnv - https://github.com/pyenv/pyenv#homebrew-on-mac-os-x

  * Add the following to ~/.bash_profile and then run `source ~/.bash_profile`.
    ```
    export PATH="/Users/username/.pyenv:$PATH"
    eval "$(pyenv init -)"
    ```
    
  * Install PyEnv
    ```
    brew update
    brew install pyenv
    pyenv --help
    pyenv install 3.6.3
    pyenv local 3.6.3
    ```
    
* Setup PyEthereum 

  * About
    * Pyethereum is the Python core library for Ethereum
    * Note: This is required for Python TestRPC `eth-testrpc` to work.
  
  * Install dependencies - https://github.com/ethereum/pyethereum/wiki/Developer-Notes
    ```
    brew install pkg-config libffi autoconf automake libtool openssl
    ```
    
  * Clone repo
    ```
    git clone https://github.com/ethereum/pyethereum/
    cd pyethereum
    ```
    
  * Avoid error https://github.com/ethereum/pyethapp/issues/209 `scrypt-1.2.0/libcperciva/crypto/crypto_aes.c:6:10: fatal error: 'openssl/aes.h' file not found`
    ```
    brew update
    brew upgrade openssl
    export LDFLAGS="-L/usr/local/opt/openssl/lib"
    export CPPFLAGS="-I/usr/local/opt/openssl/include"
    env LDFLAGS="-L$(brew --prefix openssl)/lib" CFLAGS="-I$(brew --prefix openssl)/include" pip install cryptography
    ```
    
  * Install PyEthereum dependencies 
    ```
    python setup.py install
    ```

* Setup Test Network for blockchain in new Unix Terminal Tab
  ```
  pip install eth-testrpc;  
  rm -rf ./db;
  mkdir -p db/chaindb;
  testrpc --db './db/chaindb'
  ```

* Back-end

  * Web3.py - http://web3py.readthedocs.io/en/latest/quickstart.html 
    * Install Web3.py
      ```
      pip install web3
      ```
  
  * Solidity Compiler
    * Install Solc
      * Install Solc.js - https://github.com/ethereum/solc-js#usage-on-the-command-line
        ```
        npm install -g solc
        solcjs --version
        ```
        
        * Troubleshooting 
          * Error 1.01 - Fix error when run main.py due to this line `compile_source(contract_source_code)` that results in error: `FileNotFoundError: [Errno 2] No such file or directory: 'solc': 'solc'`:
            * Fix was to rename solcjs to solc:
              ```
              cp /Users/Ls/.nvm/versions/node/v8.7.0/bin/solcjs /Users/Ls/.nvm/versions/node/v8.7.0/bin/solc
              
              solc --version
              ```
              
          * Error 1.02 - Fix error when run main.py (after fixing Error 1.01) due to this line `compile_source(contract_source_code)` that results in error: `Error: Cannot find module 'fs-extra' ... /Users/Ls/.nvm/versions/node/v8.7.0/bin/solc:6:10`            
            * Fix was to create a symlink from the `solc` executable to the `solcjs` that is installed in the NPM dependencies:
              ```
              ln -sF /Users/Ls/.nvm/versions/node/v8.7.0/lib/node_modules/solc/solcjs /Users/Ls/.nvm/versions/node/v8.7.0/bin/solc
              ```

      * Install Py-Solc (to be used by Python as a Wrapper for Solc.js)
        * https://pypi.python.org/pypi/py-solc
        * https://github.com/ethereum/py-solc
          ```
          pip install py-solc
          ```
          
  * Create Python program in main.py
  
  * Run Python CLI to experiment. Use the Simple Example in the Web3.py documentation
    * Run Python program 
      ```
      python ./scripts/src/main.py
      ```
      
    * Troubleshooting
      * Error encountered is: 
        ```
        Traceback (most recent call last):
          File "main.py", line 28, in <module>
            compiled_sol = compile_source(contract_source_code)
          File "/Users/Ls/.pyenv/versions/3.6.3/lib/python3.6/site-packages/solc/main.py", line 106, in compile_source
            stdoutdata, stderrdata, command, proc = solc_wrapper(**compiler_kwargs)
          File "/Users/Ls/.pyenv/versions/3.6.3/lib/python3.6/site-packages/solc/utils/string.py", line 85, in inner
            return force_obj_to_text(fn(*args, **kwargs))
          File "/Users/Ls/.pyenv/versions/3.6.3/lib/python3.6/site-packages/solc/wrapper.py", line 165, in solc_wrapper
            stderr_data=stderrdata,
        solc.exceptions.SolcError: An error occurred during execution
        > command: `solc --combined-json abi,asm,ast,bin,bin-runtime,clone-bin,devdoc,interface,opcodes,userdoc`
        > return code: `1`
        > stderr:

        > stdout:
        Must provide a file
        ```
      * Note: Pyethereum and [Pyethapp](https://github.com/ethereum/pyethapp/blob/287e36e49736cfd2ec150822010d0c0f4d85c781/.travis.yml) travis.yml files both use APT for solc.
