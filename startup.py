# Description: This script can be executed after startup. It checks for updates and upgrades the system if necessary.
# Works on: Ubuntu 22.04
# Author: @LucaDeppieri (Luca Deppieri)


# Import the modules
import subprocess
from os.path import exists

# Dictionary containing the ANSI escape codes for the colors used in the script
colors = {
    "green": "\033[32m",
    "yellow": "\033[33m",
    "cyan": "\033[36m",
    "reset": "\033[0m"
}


def progress_bar(progress, total):
    percent = 100 * progress / float(total)
    bar = '█' * int(percent) + '-' * (100 - int(percent))
    print(f"\r|{bar}| {percent:.2f}%", end='')
    if progress == total:
        print(colors["green"] +
              f"\r|{bar}| {percent:.2f}%" + colors["reset"], end='\n')


def run_command(command, total):
    process = subprocess.Popen(
        command.split(), stdout=subprocess.PIPE, universal_newlines=True)
    progress = 0
    for _ in iter(process.stdout.readline, ''):
        # Increment progress after each line of output
        progress += 1
        # Update the progress bar
        progress_bar(progress, total)
    # Wait for the subprocess to finish
    process.wait()


def upgrade():
    global stop  # Make the variable "stop" global

    print(colors["cyan"] + "\n>  Searching for updates..." + colors["reset"])
    # Run the command "sudo apt-get update"
    output = subprocess.check_output(
        ["sudo", "apt", "update"]).decode("utf-8")

    number_of_packages = 0
    for line in output.splitlines():
        if "packages can be upgraded" in line:
            number_of_packages = int(line.split()[0])
    if number_of_packages == 0:
        print(colors["cyan"] + ">  No updates found!\n" + colors["reset"])
        stop = True
        return
    else:
        stop = False

    # Run the command "sudo apt-get upgrade -y"
    # run_command("sudo apt-get upgrade -y", number_of_packages)
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
            ctr = 1
            for package_name in packages_to_upgrade.splitlines():
                if package_name:
                    output = subprocess.check_output(
                        ["sudo", "apt-get", "install", "-y", package_name]).decode("utf-8")
                    progress_bar(ctr, number_of_packages)
                    ctr += 1
            print(colors["cyan"] + "\n>  Upgrade completed!")
    else:
        print(colors["cyan"] + ">  No packages to upgrade!\n")
    del output  # Delete the variable "output"


def clean():
    # Ask the user if he wants to clean the system
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
if not stop:
    clean()
