#!/bin/bash

# Global Variables
runuser=$(whoami)
tempdir=$(pwd)

# Title Function
func_title(){
  clear

  # Echo Title
  echo '=========================================================================='
  echo ' SimplyDomain Setup Script | [Updated]: 2017'
  echo '=========================================================================='
  echo ' [Web]: Http://obscuritylabs.com | [Twitter]: @KillSwitch-GUI'
  echo '=========================================================================='
}



# Environment Checks
func_check_env(){
  # Check Sudo Dependency going to need that!
  if [ $(which sudo|wc -l) -eq '0' ]; then
    echo
    echo ' [ERROR]: This Setup Script Requires sudo!'
    echo '          Please Install sudo Then Run This Setup Again.'
    echo
    exit 1
  fi
}

func_install(){
# Setup virtual env
  add-apt-repository ppa:jonathonf/python-3.6
  apt-get update
  apt-get install python3.6
  # TODO: better way of doing this ?
  # python3.6 -m pip install autoenv
  # echo "source `which activate.sh`" >> ~/.bashrc
  # apt-get install python-virtualenv -y
  # virtualenv -p python3.6 --no-site-packages SD
  # source SD/bin/activate


  python3.6 -m pip install -r setup/requirements.txt

}


# Menu Case Statement
case $1 in
  *)
  func_title
  func_check_env
  func_install
  ;;

esac
