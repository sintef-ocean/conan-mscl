#!/bin/bash
echo "-----------------------------------------------------------------"
echo "BUILDING CONAN PACKAGES FOR MSCL"
echo "-----------------------------------------------------------------"

name=sintef/testing

dir=$(dirname "$0"/)

conan remove MSCL -f

rm -rf test_package/build
conan create . ${name} -s build_type=Debug -o:b multi_core=True

rm -rf test_package/build
conan create . ${name} -s build_type=Release -o:b multi_core=True
