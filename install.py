import os
import json
import time
import sys

class Install:
    def __init__(self, package_file='package.json', install_dir='node_modules'):
        self.package_file = package_file
        self.install_dir = install_dir

    def read_package_file(self):
        """
        Reads the package file (package.json by default) and returns its content.
        """
        if not os.path.exists(self.package_file):
            print(f"{self.package_file} does not exist.")
            return None
        with open(self.package_file, 'r') as file:
            return json.load(file)

    def create_install_dir(self):
        """
        Creates the installation directory (node_modules by default) if it does not exist.
        """
        if not os.path.exists(self.install_dir):
            os.makedirs(self.install_dir)

    def show_loading_animation(self, duration=0.5):
        """
        Shows a simple loading animation for the given duration (in seconds).
        """
        end_time = time.time() + duration
        loader = "|/-\\"
        while time.time() < end_time:
            for frame in loader:
                # Carriage return (\r) to return cursor to the start of the line
                sys.stdout.write(f'\rdownloading {frame}')
                sys.stdout.flush()
                time.sleep(0.1)  # Control the speed of the animation
        sys.stdout.write('\r')  # Clear the line

    def download_package(self, package_name):
        """
        "Downloads" the package by creating an empty .bin file for it in the installation directory.
        """
        self.show_loading_animation()

        package_path = os.path.join(self.install_dir, f"{package_name}.bin")
        with open(package_path, 'w') as _:
            pass
        print(f"downloading '{package_name}'")

    def install(self):
        """
        Reads dependencies from the package file and proceeds to "download" them.
        """
        package_data = self.read_package_file()
        if package_data:
            self.create_install_dir()
            dependencies = package_data.get('dependencies', {})
            for package_name in dependencies:
                self.download_package(package_name)