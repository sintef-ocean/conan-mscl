from conans import ConanFile, CMake, tools
import os

class MSCLTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = ("cmake_paths", "cmake_find_package")
    options = {"shared": [True, False]}
    default_options = {"shared": False}
    requires = "mscl/%s@sintef/testing" % (tools.load(".." + os.sep + "version.txt").strip())

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        tester_path = os.path.join(self.build_folder, "bin")
        if self.settings.os=="Windows":
            tester_exe = "TestTarget.exe"
        else:
            tester_exe = "TestTarget"
        self.run(os.path.join(tester_path, tester_exe))
