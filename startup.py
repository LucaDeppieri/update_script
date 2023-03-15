import subprocess
from os.path import exists

# Dictionary containing the ANSI escape codes for the colors used in the script
colors = {
    "yellow": "\033[33m",
    "cyan": "\033[36m",
    "reset": "\033[0m"
}


def upgrade():
    # Run the command "sudo apt-get update" and save the output in the variable "output"
    print(colors["cyan"] + "\n>  Searching for updates..." + colors["reset"])
    subprocess.run(["sudo", "apt-get", "update", "|", "grep", "-q"])

    # Run the command "sudo apt-get upgrade -y" and save the output in the variable "output"
    print(colors["cyan"] + "\n>  Upgrading..." + colors["reset"])
    subprocess.run(["sudo", "apt-get", "upgrade", "-y"])
    subprocess.run(["sudo", "apt-get", "autoremove", "-y"])
    output = subprocess.check_output(
        ["apt", "list", "--upgradable"]).decode("utf-8")

    # If the number of output lines is greater than 1, then there are upgradable packages
    if (len(output.splitlines()) > 1):
        packages_to_upgrade = ""
        for line in output.splitlines()[1:]:
            package_name = line.split("/")[0]
            packages_to_upgrade += package_name + "\n"
        print(colors["cyan"] + ">  The following packages can be upgraded:")
        print(colors["yellow"] + packages_to_upgrade + colors["cyan"])
        user_input = input("Do you want to install them? (y/n): ")
        if user_input == "y":
            print("> Upgrading..." + colors["reset"])
            for package_name in packages_to_upgrade.splitlines():
                if package_name:
                    subprocess.run(
                        ["sudo", "apt-get", "install", "-y", package_name])
            print(colors["cyan"] + "\n>  Upgrade completed!")
    else:
        print(colors["cyan"] + ">  No packages to upgrade!\n")
    del output  # Delete the variable "output"


def clean():
    # Ask the user if he wants to clean the system
    print(">  Upgrade completed!\n")
    user_input = input("Do you want to clean the system? (y/n): ")

    # If the user has entered "y", then run the commands "sudo apt-get clean" and "sudo apt-get autoremove --purge"
    if user_input == "y":
        print("\n> Cleaning..." + colors["reset"])
        subprocess.run(["sudo", "apt-get", "clean"])
        subprocess.run(["sudo", "apt-get", "autoremove", "--purge"])
        print(colors["cyan"] + "> All cleaned!\n")

    print(colors["reset"])


# Run the functions
upgrade()
clean()
