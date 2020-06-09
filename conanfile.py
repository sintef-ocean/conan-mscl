from conans import ConanFile, CMake, tools, MSBuild
import glob
import os

class MSCLConan(ConanFile):
    name = "mscl"
    license = "MIT"
    author = "LORD Corporation"
    description = "MSCL - The MicroStrain Communication Library. MSCL is developed by LORD Sensing - Microstrain in Williston, VT. It was created to make it simple to interact with our Wireless, Inertial, and digital Displacement sensors."
    topics = ("MRU API")
    homepage = "https://github.com/LORD-MicroStrain/MSCL"
    url = "http://github.com/sintef-ocean/conan-mscl"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False],
               "multi_core": [True, False]}
    default_options = {"shared": False,
                       "multi_core": False}
    generators = ("cmake_paths", "cmake_find_package")
    requires = ("boost/1.70.0","openssl/1.0.2u")
    exports = ("version.txt", "CMakeLists.txt")

    def set_version(self):
        self.version = tools.load(self.recipe_folder + os.sep + "version.txt").strip()

    def source(self):
        self.run("git clone --depth 1 -b v{0} https://github.com/LORD_MicroStrain/MSCL.git".format(self.version))

    def build(self):
        cmake = CMake(self, parallel=self.options.multi_core)
        cmake.configure()
        cmake.build()
        cmake.install()

    def package(self):
        include_path = os.path.join(self.build_folder,os.path.join("MSCL",os.path.join("MSCL","source")))
        self.copy("*.h",dst="include", src=include_path)
        self.copy("*.hpp",dst="include", src=include_path)
        self.copy("*.cmake", dst=".")
        if self.settings.os == "Windows":
            self.copy("*.lib", dst="lib", keep_path=False)
            self.copy("*.pdb", dst="lib", keep_path=False)
            self.copy("*.dll", dst="lib", keep_path=False)
        else:
            self.copy("*mscl.a", dst="lib", keep_path=False)
            self.copy("*mscl.so", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.name = "MSCL"
        self.cpp_info.libs = ["mscl"]
