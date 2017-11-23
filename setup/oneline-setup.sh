#!/usr/bin/env bash

func_check_env(){
  # Check Sudo Dependency going to need that!
  if [ $(which sudo|wc -l) -eq '0' ]; then
    echo
    echo ' [ERROR]: This Setup Script Requires sudo!'
    echo '          Please Install sudo Then Run This Setup Again.'
    echo
    exit 1
  fi

  git clone --branch master https://github.com/SimplySecurity/SimplyDomain.git
  cd SimplyDomain
  ./setup/setup.sh
}


case $1 in
  *)
  func_check_env
  ;;

esac
