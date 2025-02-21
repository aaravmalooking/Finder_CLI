from colorama import Fore, Style
from rich.tree import Tree
from rich.console import Console
import os
from pathlib import Path
import shutil


def format_size(size):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PB"


def list_dir(path="."):
    path = os.path.expanduser(path)  # Expand ~ to user's home directory
    tree = Tree(f"{path}")

    for item in os.listdir(path):
        full_path = os.path.join(path, item)
        if os.path.isdir(full_path):
            tree.add(f"{item}/")
        else:
            size = os.path.getsize(full_path)
            tree.add(f" {item} ({format_size(size)})")

    console = Console()
    console.print(tree)


class ui:
    def interface(self):
        input_cmd = input(os.getcwd() + "> ").strip()
        input_cmd = input_cmd.replace("~", os.path.expanduser("~"))
        input_cmd = input_cmd.replace("*", os.path.expanduser("~\\Desktop"))
        input_cmd = input_cmd.replace("$", os.path.expanduser("~\\Downloads"))
        input_cmd = input_cmd.replace("&", os.path.expanduser("~\\Appdata"))


        if input_cmd == "cd..":
            os.chdir("..")
            return

        if input_cmd.startswith("move "):
            try:
                # Extract arguments and split by comma
                args = input_cmd[5:].strip().split(",")

                if len(args) < 2:
                    print(Fore.RED + "Error: move command requires source and destination." + Style.RESET_ALL)
                    return


                source = args[0].strip()
                destination = args[1].strip()


                if not os.path.exists(source):
                    print(Fore.RED + f"Error: Source '{source}' does not exist." + Style.RESET_ALL)
                    return

                if os.path.isdir(destination):
                    destination = os.path.join(destination, os.path.basename(source))

                shutil.move(source, destination)
                print(Fore.GREEN + f"Moved '{source}' to '{destination}'" + Style.RESET_ALL)

            except Exception as e:
                print(Fore.RED + f"Error: {e}" + Style.RESET_ALL)
            return

        if input_cmd.startswith("cd "):
            path = input_cmd[3:].strip()
            try:
                os.chdir(path)
            except FileNotFoundError:
                print(Fore.RED + "Directory not found." + Style.RESET_ALL)
            except PermissionError:
                print(Fore.RED + "Permission denied." + Style.RESET_ALL)
            except OSError:
                print(Fore.RED + "Invalid path, please supply a valid directory." + Style.RESET_ALL)
            return

        if input_cmd.startswith("touch "):
            file_name = input_cmd[6:].strip()
            try:
                Path(file_name).touch()
            except Exception as e:
                print(Fore.RED + f"Error: {e}" + Style.RESET_ALL)
            return

        if input_cmd == "ls":
            list_dir()
            return

        if input_cmd == "tutor":
            print("Welcome to Finder_CLI tutorial!")
            print("Finder_CLI is a command-line-based file explorer for programmers.")
            print("Basic commands include cd, ls, move, touch, and more.")
            print("Use ~ to refer to your home folder (C:\\Users\\YourName).")
            return

        else:
            print(Fore.RED + "finder_cli command syntax or the command is invalid, please try again" + Style.RESET_ALL)


ui_obj = ui()

if __name__ == "__main__":
    while True:
        ui_obj.interface()
