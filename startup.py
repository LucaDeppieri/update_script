import subprocess
from os.path import exists

# Dizioneario contenente i colori
colors = {
    "yellow": "\033[33m",
    "cyan": "\033[36m",
    "reset": "\033[0m"
}

print(colors["cyan"] + "\n###  Aggiornamento in corso..." + colors["reset"])

# Esegui il comando "sudo apt update", "sudo apt upgrade -y", "sudo apt autoremove -y" e "apt list --upgradable"
subprocess.run(["sudo", "apt", "update"])
subprocess.run(["sudo", "apt", "upgrade", "-y"])
subprocess.run(["sudo", "apt", "autoremove", "-y"])
output = subprocess.check_output(
    ["apt", "list", "--upgradable"]).decode("utf-8")

# Se il numero di righe di output è maggiore di 1, allora ci sono pacchetti aggiornabili
if (len(output.splitlines()) > 1):
    if exists("upgradable.txt"):
        with open("upgradable.txt", "r+") as file:
            file.truncate(0)
    with open("upgradable.txt", "w") as file:
        for line in output.splitlines()[1:]:
            package_name = line.split("/")[0]
            file.write(package_name + "\n")
    with open("upgradable.txt", "r") as file:
        print(colors["cyan"] +
              "###  I seguenti pacchetti sono aggiornabili:")
        print(colors["yellow"])
        for line in file:
            print(line)
        print(colors["cyan"])
    user_input = input("Vuoi installarli? (y/n): ")
    if user_input == "y":
        print("### Installazione in corso..." + colors["reset"])
        with open("upgradable.txt", "r") as file:
            for line in file:
                subprocess.run(["sudo", "apt", "install", "-y", line])
        print(colors["cyan"] + "\n###  Installazione completata!")
else:
    print(colors["cyan"] + "###  Nessun pacchetto aggiuntivo da installare!")

# Domanda all'utente se vuole ripulire il sistema
print("###  Aggiornamento completato!\n")
user_input = input("Vuoi pulire il sistema? (y/n): ")

# Se l'utente ha inserito "y", allora esegui il comando "sudo apt clean" e "sudo apt autoremove --purge"
if user_input == "y":
    print("\n### Pulizia in corso..." + colors["reset"])
    subprocess.run(["sudo", "apt", "clean"])
    subprocess.run(["sudo", "apt", "autoremove", "--purge"])
    print(colors["cyan"] + "### Pulizia completata!\n")

print(colors["reset"])
