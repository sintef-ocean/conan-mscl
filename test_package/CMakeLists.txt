cmake_minimum_required(VERSION 3.6)
project(mscl-test)

set (CMAKE_CXX_STANDARD 11)
if (UNIX)
    add_compile_options("-Wl,-V")
endif()

message(STATUS "Using Conan to build...")
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()
message(STATUS "*** LIB_DIRS: ${CONAN_LIB_DIRS}")
message(STATUS "*** LIBS: ${CONAN_LIBS}")

include_directories(${CONAN_INCLUDE_DIRS})
set(TESTER "TestTarget")

set( SRC
    ${CMAKE_SOURCE_DIR}/src/getCurrentConfig.h
    ${CMAKE_SOURCE_DIR}/src/main.cpp
    ${CMAKE_SOURCE_DIR}/src/parseData.h
    ${CMAKE_SOURCE_DIR}/src/setCurrentConfig.h
    ${CMAKE_SOURCE_DIR}/src/setToIdle.h
    ${CMAKE_SOURCE_DIR}/src/startSampling.h)


add_executable(${TESTER} ${SRC})
#target_compile_definitions(${TESTER} PUBLIC BOOST_NO_CXX11_SCOPED_ENUMS)
target_include_directories(${TESTER} PRIVATE ${CONAN_INCLUDE_DIRS} ${CMAKE_SOURCE_DIR}/src)
target_link_directories(${TESTER} PRIVATE ${CONAN_LIB_DIRS})
target_link_libraries(${TESTER} PRIVATE  ${CONAN_LIBS})
