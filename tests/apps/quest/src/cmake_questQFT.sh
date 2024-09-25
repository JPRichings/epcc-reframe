#!/bin/bash

TARGET=${1}
BUILD_DIR=build
SOURCE_DIR=QuEST

mkdir -p ${BUILD_DIR}
cd ${BUILD_DIR}

USER_SOURCE=../${TARGET}.cpp
OUTPUT_EXE=${TARGET}
DISTRIBUTED=1
MULTITHREADED=1
GPUACCELERATED=0

CC=cc
CXX=CC

cmake ../${SOURCE_DIR} \
  -DCMAKE_C_COMPILER=${CC} \
  -DCMAKE_CXX_COMPILER=${CXX} \
  -DUSER_SOURCE=${USER_SOURCE} \
  -DOUTPUT_EXE=${OUTPUT_EXE} \
  -DDISTRIBUTED=${DISTRIBUTED} \
  -DMULTITHREADED=${MULTITHREADED} \
  -DGPUACCELERATED=${GPUACCELERATED}
