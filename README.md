# Conan package recipe and package test for MSCL
To create the package and run the `test_package` recipe, simply run
```bash
conan create . sintef/testing -s build_type=<Release|Debug>
```
This will build the `(lib)mscl.(a)lib` file and install it in your local .conan repository.
Also, it will compile and run a tester.
NB!! Note that the tester will fail if a MRU is not connected to `COM4`.
However, if the tester nags about wrong COM-port, the conan package is working.
Note that this test should be improved later on.

## Including the MSCL-API
For more information about how to include the MSCL-API in your project, see the corresponding cmake- and conan files in the `test_package` folder.
