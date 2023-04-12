# Description: This script can be executed after startup. It checks for updates and upgrades the system if necessary.
# Works on: Ubuntu 22.04
# Author: @LucaDeppieri (Luca Deppieri)


# Import the modules
import subprocess
from time import sleep

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


def upgrade():
    global stop  # Make the variable "stop" global

    print(colors["cyan"] + "\n[run] " + colors["reset"] + "sudo apt update")
    # Run the command "sudo apt update"
    output = subprocess.check_output(["sudo", "apt", "update"]).decode("utf-8")
    for line in output.splitlines():
        print(line)
        sleep(0.1)

    number_of_packages = 0
    for line in output.splitlines():
        if "packages can be upgraded" in line:
            number_of_packages = int(line.split()[0])
    if number_of_packages == 0:
        print(colors["cyan"] + "\n[info] " +
              colors["reset"] + "No updates found!\n")
        stop = True
        return
    else:
        stop = False

    # Run the command "sudo apt-get upgrade -y"
    print(colors["cyan"] + "\n[run] " +
          colors["reset"] + "sudo apt-get upgrade -y")
    subprocess.run(["sudo", "apt-get", "upgrade", "-y"])
    print(colors["cyan"] + "\n[run] " + colors["reset"] +
          "sudo apt autoremove -y")
    subprocess.run(["sudo", "apt-get", "autoremove", "-y"])
    print(colors["cyan"] + "\n[run] " +
          colors["reset"] + "apt list --upgradable")
    subprocess.run(["apt", "list", "--upgradable", "2>/dev/null"])

    # If the number of output lines is greater than 1, then there are upgradable packages
    if (len(output.splitlines()) > 1):
        packages_to_upgrade = ""
        for line in output.splitlines()[1:]:
            package_name = line.split("/")[0]
            packages_to_upgrade += package_name + "\n"
        print(colors["cyan"] + "[info] " + colors["reset"] +
              "The following packages can be upgraded:")
        print(colors["yellow"] + packages_to_upgrade + colors["reset"])
        user_input = input("Do you want to install them? (y/n): ")

        if user_input == "y":
            print(colors["cyan"] + "[info] " +
                  "Upgrading..." + colors["reset"])
            ctr = 1
            for package_name in packages_to_upgrade.splitlines():
                print(colors["cyan"] + "\n[run] " + colors["reset"] +
                      "sudo apt install -y " + package_name)
            for package_name in packages_to_upgrade.splitlines():
                if package_name:
                    output = subprocess.check_output(
                        ["sudo", "apt-get", "install", "-y", package_name]).decode("utf-8")
                    progress_bar(ctr, number_of_packages)
                    ctr += 1
            progress_bar(number_of_packages, number_of_packages)
            print(colors["cyan"] + "\n[info] " +
                  colors["reset"] + "Upgrade completed!")
    else:
        print(colors["cyan"] + "[info] " +
              colors["reset"] + "No packages to upgrade!\n")


def clean():
    # Ask the user if he wants to clean the system
    user_input = input(colors["cyan"] + "[request] " +
                       colors["reset"] + "Do you want to clean the system? (y/n): ")

    # If the user has entered "y", then run the commands "sudo apt-get clean" and "sudo apt-get autoremove --purge"
    if user_input == "y":
        print(colors["cyan"] + "\n[info] " +
              colors["reset"] + "Cleaning..." + colors["reset"])
        print(colors["cyan"] + "\n[run] " +
              colors["reset"] + "sudo apt-get clean")
        subprocess.run(["sudo", "apt-get", "clean"])
        print(colors["cyan"] + "\n[run] " + colors["reset"] +
              "sudo apt-get autoremove --purge")
        subprocess.run(["sudo", "apt-get", "autoremove", "--purge"])
        print(colors["cyan"] + "[info] " + colors["reset"] + "All cleaned!\n")


# Run the functions
upgrade()
if not stop:
    clean()
