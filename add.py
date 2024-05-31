import os
import argparse
import json

class Add:
    def __init__(self, dependency_lookup_file):
        self.dependency_lookup = self.load_dependency_lookup(dependency_lookup_file)

    def get_script_directory(self):
        return os.path.dirname(os.path.realpath(__file__))

    def load_dependency_lookup(self, dependency_lookup_file):
        script_dir = self.get_script_directory()
        dependency_lookup_path = os.path.join(script_dir, dependency_lookup_file)
        with open(dependency_lookup_path, "r") as f:
            return json.load(f)

    def find_package(self, name, version):
        for package in self.dependency_lookup:
            if package["name"] == name and package["version"] == version:
                return package
        return None

    def get_higher_version(self, version1, version2):
        return max(version1, version2, key=lambda v: [int(part) for part in v.split('.')])

    def add_dependencies(self, package_json, package):
        for dep_name, dep_info in package["dependencies"].items():
            if dep_name not in package_json["dependencies"]:
                package_json["dependencies"][dep_name] = dep_info["version"]
            else:
                existing_version = package_json["dependencies"][dep_name]
                higher_version = self.get_higher_version(existing_version, dep_info["version"])
                package_json["dependencies"][dep_name] = higher_version

            dep_package = self.find_package(dep_name, package_json["dependencies"][dep_name])
            if dep_package:
                self.add_dependencies(package_json, dep_package)

    def add(self, name, version):
        package_json_path = "package.json"
        if os.path.exists(package_json_path):
            with open(package_json_path, "r") as f:
                package_json = json.load(f)
        else:
            package_json = {
                "name": "my_project",
                "version": "1.0.0",
                "dependencies": {}
            }

        package = self.find_package(name, version)
        if not package:
            print(f"Package {name} version {version} not found in the dependency lookup table.")
            return

        if name not in package_json["dependencies"]:
            package_json["dependencies"][name] = version
        else:
            existing_version = package_json["dependencies"][name]
            higher_version = self.get_higher_version(existing_version, version)
            package_json["dependencies"][name] = higher_version

        self.add_dependencies(package_json, package)

        with open(package_json_path, "w") as f:
            json.dump(package_json, f, indent=4)

        print(f"Package {name} version {version} added successfully.")