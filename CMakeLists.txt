cmake_minimum_required(VERSION 3.6)
file(STRINGS "${CMAKE_CURRENT_SOURCE_DIR}/version.txt" projectVersion)
project("MSCL"
        VERSION ${projectVersion}
        LANGUAGES CXX
        DESCRIPTION "MSCL - The MicroStrain Communication Library.")

set(CMAKE_CXX_EXTENSIONS OFF) # Disable compiler flag extension (use -std=c++14 instead of -std=gnu++14)
set(CMAKE_CXX_STANDARD 14) # The default CXX_STANDARD (resolves to a flag -std=c++14)..
set(CMAKE_CXX_STANDARD_REQUIRED ON)

message(STATUS "Using Conan to build...")
include(${CMAKE_BINARY_DIR}/conan_paths.cmake)

find_package(Boost MODULE REQUIRED)
find_package(OpenSSL MODULE REQUIRED)

if (UNIX)
    set(EXCLUDES
        "${CMAKE_CURRENT_SOURCE_DIR}/MSCL/MSCL/source/mscl/Communication/WsdaFinder.cpp"
        "${CMAKE_CURRENT_SOURCE_DIR}/MSCL/MSCL/source/mscl/Communication/UpnpService.h"
        "${CMAKE_CURRENT_SOURCE_DIR}/MSCL/MSCL/source/mscl/Communication/UpnpService.cpp"
        "${CMAKE_CURRENT_SOURCE_DIR}/MSCL/MSCL/source/mscl/Communication/UpnpDeviceFinderCallback.h"
        "${CMAKE_CURRENT_SOURCE_DIR}/MSCL/MSCL/source/mscl/Communication/UpnpDeviceFinderCallback.cpp")
else()
    set(EXCLUDES
        "${CMAKE_CURRENT_SOURCE_DIR}/MSCL/MSCL/source/mscl/Communication/UnixSocketConnection.cpp"
        "${CMAKE_CURRENT_SOURCE_DIR}/MSCL/MSCL/source/stdafx.h")
    macro(get_WIN32_WINNT version)
        if(CMAKE_SYSTEM_VERSION)
            set(ver ${CMAKE_SYSTEM_VERSION})
            string(REGEX MATCH "^([0-9]+).([0-9])" ver ${ver})
            string(REGEX MATCH "^([0-9]+)" verMajor ${ver})
            # Check for Windows 10, b/c we'll need to convert to hex 'A'.
            if("${verMajor}" MATCHES "10")
                set(verMajor "A")
                string(REGEX REPLACE "^([0-9]+)" ${verMajor} ver ${ver})
            endif()
            # Remove all remaining '.' characters.
            string(REPLACE "." "" ver ${ver})
            # Prepend each digit with a zero.
            string(REGEX REPLACE "([0-9A-Z])" "0\\1" ver ${ver})
            set(${version} "0x${ver}")
        endif()
    endmacro()
    get_WIN32_WINNT(ver)
    add_definitions(-D_WIN32_WINNT=${ver})
endif()
file(GLOB_RECURSE SOURCES "${CMAKE_CURRENT_SOURCE_DIR}/MSCL/MSCL/source/*.cpp")

foreach (excl ${EXCLUDES})
    list(REMOVE_ITEM SOURCES "${excl}")
    message("Excluding ${excl}")
endforeach()

add_library(mscl STATIC ${SOURCES})
target_include_directories(mscl PRIVATE "${CONAN_INCLUDE_DIRS}" "${CMAKE_CURRENT_SOURCE_DIR}/MSCL/MSCL/source")
target_link_libraries(mscl PUBLIC Boost::Boost PRIVATE OpenSSL::OpenSSL)
if (UNIX)
    target_compile_definitions(mscl PUBLIC UNIX_BUILD)
endif()

target_include_directories(mscl PUBLIC "$<INSTALL_INTERFACE:include>")

# ==========================================
# Export config
# ==========================================

install(TARGETS mscl
   EXPORT ${CMAKE_PROJECT_NAME}
   ARCHIVE DESTINATION lib
   RUNTIME DESTINATION bin
   LIBRARY DESTINATION lib
   INCLUDES DESTINATION include)

include(CMakePackageConfigHelpers)
set(INSTALL_CONFIGDIR "cmake")
configure_package_config_file(${CMAKE_CURRENT_SOURCE_DIR}/cmake/${CMAKE_PROJECT_NAME}Config.cmake.in
    ${CMAKE_CURRENT_BINARY_DIR}/${CMAKE_PROJECT_NAME}Config.cmake
                              PATH_VARS INSTALL_CONFIGDIR
                              INSTALL_DESTINATION ".")

install(EXPORT
        ${CMAKE_PROJECT_NAME}
        DESTINATION "${INSTALL_CONFIGDIR}"
        NAMESPACE "${CMAKE_PROJECT_NAME}::"
        FILE "${CMAKE_PROJECT_NAME}Targets.cmake")

export( EXPORT
        ${CMAKE_PROJECT_NAME}
        NAMESPACE MSCL::
        FILE "${INSTALL_CONFIGDIR}/${CMAKE_PROJECT_NAME}Targets.cmake")

install(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/${INSTALL_CONFIGDIR} DESTINATION "." PATTERN *swp EXCLUDE PATTERN *.in EXCLUDE)
install(FILES ${CMAKE_CURRENT_BINARY_DIR}/${CMAKE_PROJECT_NAME}Config.cmake DESTINATION ".")
install(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/MSCL/MSCL/source/ DESTINATION include FILES_MATCHING PATTERN "*.h")
