import pkg_resources

print("Config File Runing...")  # Debugging line

def list_installed_packages():
    installed_packages = pkg_resources.working_set
    for package in installed_packages:
        print(f"{package.key} == {package.version}")

# Call the function to execute
list_installed_packages()