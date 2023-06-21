from os import path
from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.microsoft import check_min_vs, is_msvc_static_runtime, is_msvc
from conan.tools.files import get, copy, rm, rmdir, replace_in_file, load
from conan.tools.build import check_min_cppstd
from conan.tools.scm import Version
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.env import VirtualBuildEnv

required_conan_version = ">=1.53.0"

class MSCLConan(ConanFile):
    name = "mscl"
    license = "MIT"
    author = "SINTEF Ocean"
    description = \
            "MSCL - The MicroStrain Communication Library. "\
            "MSCL is developed by LORD Sensing - Microstrain in Williston, VT. "\
            "It was created to make it simple to interact with our Wireless, "\
            "Inertial, and digital Displacement sensors."
    topics = ("MRU API", "MicroStrain")
    homepage = "https://github.com/LORD-MicroStrain/MSCL"
    url = "http://github.com/sintef-ocean/conan-mscl"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "fPIC": [True, False]
    }
    default_options = {
        "shared": False,
        "fPIC": True
    }

    @property
    def _min_cppstd(self):
        return 14

    @property
    def _compilers_minimum_version(self):
        return {
            "msvc": "14.0",
            "gcc": "5",
            "clang": "5",
            "apple-clang": "5.1",
        }

    def set_version(self):
        self.version = load(
            self,
            path.join(self.recipe_folder,"version.txt")).strip()

    def export(self):
        for fil in ["version.txt"]:
            copy(self, fil, self.recipe_folder, self.export_folder)

    def export_sources(self):
        for fil in ["version.txt", "CMakeLists.txt"]:
            copy(self, fil, self.recipe_folder, self.export_sources_folder)

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def layout(self):
        cmake_layout(self, src_folder=".")

    def requirements(self):
        self.requires("boost/[>=1.78.0 <1.82.0]")
        self.requires("openssl/[>=1.1 <4]")

    def validate(self):
        if self.settings.compiler.cppstd:
            check_min_cppstd(self, self._min_cppstd)
        check_min_vs(self, 190)
        if not is_msvc(self):
            minimum_version = self._compilers_minimum_version.get(str(self.settings.compiler), False)
            if minimum_version and Version(self.settings.compiler.version) < minimum_version:
                raise ConanInvalidConfiguration(
                    f"{self.ref} requires C++{self._min_cppstd}, which your compiler does not support."
                )

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True, destination="MSCL")
        for f in ["MSCL/source/stdafx.h", "MSCL/source/mscl/Endianness.h", "MSCL_Unit_Tests/Test_Utils.cpp"]:
            replace_in_file(
                self,
                path.join(self.source_folder, "MSCL", f),
                "boost/detail/endian.hpp",
                "boost/predef/other/endian.h")

        for f in ["MSCL/source/mscl/Endianness.h", "MSCL_Unit_Tests/Test_Utils.cpp"]:
            replace_in_file(
                self,
                path.join(self.source_folder, "MSCL", f),
                "BOOST_LITTLE_ENDIAN",
                "BOOST_ENDIAN_LITTLE_BYTE")

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()

        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["mscl"]
