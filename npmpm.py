import os
import argparse

import add
import install

super_duper_secret = "2372839uoegfqweoir812931asdf"

add_object = add.Add("dependency_lookup.json")

install_object = install.Install()

def get_args():
    parser = argparse.ArgumentParser(description="Process some package operations.")
    parser.add_argument("operation", choices=["add", "install"], help="The operation to perform")
    
    # Make 'package' an optional argument
    parser.add_argument("package", nargs="?", default=None, help="The package name with version in the format <package-name>@<version> (required for add operation)")

    args = parser.parse_args()

    operation = args.operation
    package = args.package

    # Split the package into name and version if it is not None
    if package:
        if "@" in package:
            package_name, version = package.split("@", 1)
        else:
            package_name = package
            version = None
    else:
        package_name, version = None, None

    # For the 'install' operation, package name is not needed
    if operation == "install" and package_name is not None:
        print("'install' operation does not require a package argument.")
        exit(1)

    return operation, package_name, version


operation, package_name, version = get_args()

if operation == "add":
    if package_name is None or version is None:
        print("Adding a package requires specifying the package name and version.")
    else:
        add_object.add(package_name, version)

elif operation == 'install':
    install_object.install()

else:
    print(operation, "is not a valid operation")