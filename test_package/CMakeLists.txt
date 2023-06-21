cmake_minimum_required(VERSION 3.15)
project(mscl-test)

set(TESTER "TestTarget")
find_package(mscl CONFIG REQUIRED)

set(SRC
    ${CMAKE_SOURCE_DIR}/src/getCurrentConfig.h
    ${CMAKE_SOURCE_DIR}/src/main.cpp
    ${CMAKE_SOURCE_DIR}/src/parseData.h
    ${CMAKE_SOURCE_DIR}/src/setCurrentConfig.h
    ${CMAKE_SOURCE_DIR}/src/setToIdle.h
    ${CMAKE_SOURCE_DIR}/src/startSampling.h)

add_executable(${TESTER} ${SRC})
target_link_libraries(${TESTER} PUBLIC mscl::mscl)
target_compile_features(${TESTER} PRIVATE cxx_std_14)
