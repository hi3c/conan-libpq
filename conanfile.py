from conans import ConanFile, CMake, tools, AutoToolsBuildEnvironment
import os
import shutil


class LibpqConan(ConanFile):
    name = "libpq"
    version = "9.6.3_1"
    license = "<Put the package license here>"
    url = "<Package recipe repository url here, for issues about the package>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "cmake"
    exports = "CMakeLists.txt", "pg_config_paths.h"
    requires = "OpenSSL/1.0.2l@conan/stable"

    @property
    def source_dir(self):
        return os.path.join("postgresql-9.6.3", "src", "interfaces", "libpq")

    def source(self):
        tools.download("https://ftp.postgresql.org/pub/source/v9.6.3/postgresql-9.6.3.tar.bz2",
                       "postgresql.tar.bz2")
        tools.unzip("postgresql.tar.bz2")
        os.remove("postgresql.tar.bz2")

        shutil.copy("CMakeLists.txt", self.source_dir)

    def build(self):
        if self.settings.os == "Windows":
          cmake = CMake(self)
          cmake.configure(source_dir=self.source_dir)
          cmake.build()
        else:
          atbe = AutoToolsBuildEnvironment(self)
          atbe.configure(configure_dir="postgresql-9.6.3", args=["--with-openssl", "--without-readline"])
          atbe.make(["-C", os.path.join("src", "interfaces", "libpq")])

    def package(self):
        self.copy("*.h", src=self.source_dir, dst="include")
        self.copy("*.h", src=os.path.join("postgresql-9.6.3", "src", "include"), dst="include")
        self.copy("*.h", src="src/include", dst="include")

        self.copy("*.lib", dst="lib", src="lib")

        if self.options.shared:
            self.copy("*.dll", dst="bin", src="bin")
            self.copy("*.so*", dst="lib", src="src/interfaces/libpq")
            self.copy("*.dylib", dst="lib", src="src/interfaces/libpq")
        else:
            self.copy("*.a", dst="lib", src="lib")

    def package_info(self):
        if self.settings.os == "Windows":
            self.cpp_info.libs = ["libpqdll"]
        else:
            self.cpp_info.libs = ["pq"]
