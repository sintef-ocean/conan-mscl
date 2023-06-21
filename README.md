[![Linux GCC](https://github.com/sintef-ocean/conan-mscl/workflows/Linux%20GCC/badge.svg)](https://github.com/sintef-ocean/conan-mscl/actions?query=workflow%3A"Linux+GCC")
[![Linux Clang](https://github.com/sintef-ocean/conan-mscl/workflows/Linux%20Clang/badge.svg)](https://github.com/sintef-ocean/conan-mscl/actions?query=workflow%3A"Linx+Clang")
[![Windows MSVC](https://github.com/sintef-ocean/conan-mscl/workflows/Windows%20MSVC/badge.svg)](https://github.com/sintef-ocean/conan-mscl/actions?query=workflow%3A"Windows+MSVC")

[Conan.io](https://conan.io) recipe for [MSCL](https://github.com/LORD-MicroStrain/MSCL).

## How to use this package

1. Add remote to conan's package [remotes](https://docs.conan.io/2/reference/commands/remote.html)

   ```bash
   $ conan remote add sintef https://artifactory.smd.sintef.no/artifactory/api/conan/conan-local
   ```

2. Using [*conanfile.txt*](https://docs.conan.io/2/reference/conanfile_txt.html) and *cmake* in your project.

   Add *conanfile.txt*:

   ```
   [requires]
   mscl/64.2.2@sintef/stable

   [tool_requires]
   cmake/[>=3.25.0]

   [options]

   [layout]
   cmake_layout

   [generators]
   CMakeDeps
   CMakeToolchain
   VirtualBuildEnv
   ```
   Insert into your *CMakeLists.txt* something like the following lines:
   ```cmake
   cmake_minimum_required(VERSION 3.15)
   project(TheProject CXX)

   find_package(mscl CONFIG REQUIRED)

   add_executable(the_executor code.cpp)
   target_link_libraries(the_executor mscl::mscl)
   ```
   Install and build e.g. a Release configuration:
   ```bash
   $ conan install . -s build_type=Release -pr:b=default
   $ source build/Release/generators/conanbuild.sh
   $ cmake --preset conan-release
   $ cmake --build build/Release
   $ source build/Release/generators/deactivate_conanbuild.sh
   ```

## Package options

| Option        | Allowed values    |   Default value   |
| ------------- | ----------------- | ----------------- |
| shared        | [True, False]     | False             |
| fPIC          | [True, False]     | True              |

## Known recipe issues

None
