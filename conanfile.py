from conans import ConanFile, CMake, tools
import os

class MSCLConan(ConanFile):
    name = "mscl"
    license = "MIT"
    author = "Stian Skjong (stian.skjong@sintef.no)"
    description = \
            "MSCL - The MicroStrain Communication Library. "\
            "MSCL is developed by LORD Sensing - Microstrain in Williston, VT. "\
            "It was created to make it simple to interact with our Wireless, "\
            "Inertial, and digital Displacement sensors."
    topics = ("MRU API", "MicroStrain")
    homepage = "https://github.com/LORD-MicroStrain/MSCL"
    url = "http://github.com/sintef-ocean/conan-mscl"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False],
            #"multi_core": [True, False],
            "fPIC": [True, False]}
    default_options = {"shared": False,
            #"multi_core": False,
            "fPIC": True}
    generators = ("cmake_paths", "cmake_find_package")
    requires = ("boost/1.69.0", "openssl/1.1.1n")
    exports = ("version.txt", "CMakeLists.txt")
    exports_sources = "*"

    def set_version(self):
        self.version = tools.load(
                self.recipe_folder + os.sep + "version.txt").strip()

    def source(self):
        tools.get("https://github.com/LORD-MicroStrain/MSCL/archive/v{}.tar.gz"
                .format(self.version), strip_root=True, destination="MSCL")

    def configure(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def build(self):
        cmake = CMake(self)#, parallel=self.options.multi_core)
        if self.settings.os != "Windows":
            cmake.definitions['CMAKE_POSITION_INDEPENDENT_CODE'] = self.options.fPIC
        cmake.configure(source_folder=self.build_folder)
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["mscl"]
        self.user_info.DIR = ("{}"
                .format(self.package_folder)).replace("\\", "/")
