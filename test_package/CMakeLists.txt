cmake_minimum_required(VERSION 3.13)
project(mscl-test)

set(CMAKE_CXX_EXTENSIONS OFF) # Disable compiler flag extension (use -std=c++11 instead of -std=gnu++11)
set(CMAKE_CXX_STANDARD 14) # The default CXX_STANDARD (resolves to a flag -std=c++17)..
set(CMAKE_CXX_STANDARD_REQUIRED ON)

message(STATUS "Using Conan to build...")
include(${CMAKE_BINARY_DIR}/conan_paths.cmake)

set(TESTER "TestTarget")
find_package(MSCL CONFIG REQUIRED)

set( SRC
    ${CMAKE_SOURCE_DIR}/src/getCurrentConfig.h
    ${CMAKE_SOURCE_DIR}/src/main.cpp
    ${CMAKE_SOURCE_DIR}/src/parseData.h
    ${CMAKE_SOURCE_DIR}/src/setCurrentConfig.h
    ${CMAKE_SOURCE_DIR}/src/setToIdle.h
    ${CMAKE_SOURCE_DIR}/src/startSampling.h)

add_executable(${TESTER} ${SRC})
target_link_libraries(${TESTER} PUBLIC MSCL::mscl)
