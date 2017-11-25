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
  testrpc --account '0x0000000000000000000000000000000000000000000000000000000000000001, 10002471238800000000000' \
                  --account '0x0000000000000000000000000000000000000000000000000000000000000002, 10004471238800000000000' \
                  --account '0x0000000000000000000000000000000000000000000000000000000000000003, 10004471238800000000000' \
                  --account '0x0000000000000000000000000000000000000000000000000000000000000004, 10004471238800000000000' \
                  --account '0x0000000000000000000000000000000000000000000000000000000000000005, 10004471238800000000000' \
                  --account '0x0000000000000000000000000000000000000000000000000000000000000006, 10004471238800000000000' \
                  --account '0x0000000000000000000000000000000000000000000000000000000000000007, 10004471238800000000000' \
                  --unlock '0x0000000000000000000000000000000000000000000000000000000000000001' \
                  --unlock '0x0000000000000000000000000000000000000000000000000000000000000002' \
                  --unlock '0x0000000000000000000000000000000000000000000000000000000000000003' \
                  --unlock '0x0000000000000000000000000000000000000000000000000000000000000004' \
                  --unlock '0x0000000000000000000000000000000000000000000000000000000000000005' \
                  --unlock '0x0000000000000000000000000000000000000000000000000000000000000006' \
                  --unlock '0x0000000000000000000000000000000000000000000000000000000000000007' \
                  --unlock '0x7e5f4552091a69125d5dfcb7b8c2659029395bdf' \
                  --unlock '0x2b5ad5c4795c026514f8317c7a215e218dccd6cf' \
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

* Back-end

  * Web3.py - http://web3py.readthedocs.io/en/latest/quickstart.html 
    * Install Web3.py
      ```
      pip install web3
      ```
      
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

      * Install Py-Solc (Wrapper for Solc)
        * https://pypi.python.org/pypi/py-solc
        * https://github.com/ethereum/py-solc
          ```
          pip install py-solc
          ```
          
  * Create Python program in main.py
  
  * Run Python CLI to experiment. Use the Simple Example in the Web3.py documentation
    * Run Python program 
      ```
      python main.py
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

* TODO - Testing with PyTest  
* TODO - Front-End with Truffle

* Reference 
  * Finality - https://blog.ethereum.org/2016/05/09/on-settlement-finality/
  
* Other References
  * Cloud9 / Linux PyEthereum - https://forum.ethereum.org/discussion/comment/16737#Comment_16737
  * Cloud9 / Linux PyEthereum - http://joeysprogrammingblog.com/tag/pyethereum/