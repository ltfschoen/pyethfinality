#!/usr/bin/env python

import sys, os

# allow running program from PyEthFinality main directory
# called code/ and the subdirectory
if "/".join(os.getcwd().split("/")[-1:]) == "code": # current folder name
    use_path = os.getcwd() + "/scripts/src"
elif "/".join(os.getcwd().split("/")[-1:]) == "scripts": # current folder name
    use_path = os.getcwd() + "/src"

# IMPORT CUSTOM FILES

import site
def get_main_path():
    app_path = sys.path[0] # sys.path[0] is current path in subdirectory
    split_on_char = "/"
    return split_on_char.join(app_path.split(split_on_char)[:-1])
main_path = get_main_path()
print('Main path in Docker container is: {}'.format(main_path))
site.addsitedir(main_path+'/scripts/lib')

import demo_greeting
import demo_mockchain

def main():
    # print('Running Demo - Greeting')
    # demo_greeting.run()
    print('Running Demo - Mockchain')
    demo_mockchain.run()

if __name__ == '__main__':
    main()