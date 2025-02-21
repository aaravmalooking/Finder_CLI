from colorama import Fore, Style
from rich.tree import Tree
from rich.console import Console
import os
from pathlib import Path
import shutil
import shlex


def format_size(size):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PB"




def list_dir(path="."):
    path = os.path.expanduser(path)
    tree = Tree(f"{path}")

    for item in os.scandir(path):
        full_path = os.path.join(path, item)
        if os.path.isdir(full_path):
            tree.add(f"{item}/")
        else:
            size = os.path.getsize(full_path)
            tree.add(f" {item} ({format_size(size)})")

    console = Console()
    console.print(tree)



def rm(args):
    if not args:
        print(Fore.RED + "Error: No filename specified." + Style.RESET_ALL)
    filename = args[0].strip()
    try:
        os.unlink(filename)
    except FileNotFoundError:
        print(Fore.RED + f"file specified in stdin is not found." + Style.RESET_ALL)
    except PermissionError:
        print(Fore.RED + "permission denied by operating system.")
    return



def rmdir(args):
    if not args:
        print(Fore.RED + "Error: No folder name specified." + Style.RESET_ALL)
    filename = args[0].strip()
    try:
        os.rmdir(filename)
    except FileNotFoundError:
        print(Fore.RED + f"folder specified in stdin is not found.")
    except PermissionError:
        print(Fore.RED + "permission denied by operating system.")
    return





def move_file(args):
    if len(args) < 2:
        print(Fore.RED + "Error: move command requires source and destination." + Style.RESET_ALL)
        return

    source, destination = args[0].strip(), args[1].strip()
    if not os.path.exists(source):
        print(Fore.RED + f"Error: Source '{source}' does not exist." + Style.RESET_ALL)
        return

    if os.path.isdir(destination):
        destination = os.path.join(destination, os.path.basename(source))

    shutil.move(source, destination)
    print(Fore.GREEN + f"Moved '{source}' to '{destination}'" + Style.RESET_ALL)




def change_directory(args):
    if not args:
        print(Fore.RED + "Error: No directory specified." + Style.RESET_ALL)
        return

    path = args[0].strip()



    try:
        os.chdir(path)
    except FileNotFoundError:
        print(Fore.RED + "Directory not found." + Style.RESET_ALL)
    except PermissionError:
        print(Fore.RED + "Permission denied." + Style.RESET_ALL)
    except OSError:
        print(Fore.RED + "Invalid path, please supply a valid directory." + Style.RESET_ALL)



def create_file(args):
    if not args:
        print(Fore.RED + "Error: No filename specified." + Style.RESET_ALL)
        return

    file_name = args[0].strip()
    try:
        Path(file_name).touch()
    except Exception as e:
        print(Fore.RED + f"Error: {e}" + Style.RESET_ALL)



def show_tutorial(_):
    print("Welcome to Finder_CLI tutorial!")
    print("Finder_CLI is a command-line-based file explorer for programmers.")
    print("Basic commands include cd, ls, move, touch, and more.")
    print("Use ~ to refer to your home folder (C:\\Users\\YourName).")



COMMANDS = {
    "ls": lambda _: list_dir(),
    "move": move_file,
    "cd": change_directory,
    "touch": create_file,
    "tutor": show_tutorial,
    "rm": rm,
    # "rmdir": rmdir,

}


def parse_command():

    raw_command = input(os.getcwd() + "> ").strip()



    if raw_command == "cd..":
        os.chdir("..")

        return


    try:
        parts = shlex.split(raw_command, posix=False)
    except ValueError:
        print(Fore.RED + "Error: Invalid command syntax (check quotes)." + Style.RESET_ALL)
        return

    if not parts:
        return

    cmd = parts[0]
    args = parts[1:] if len(parts) > 1 else []


    replacements = {
        "~": os.path.expanduser("~"),
        "*": os.path.expanduser("~/Desktop"),
        "$": os.path.expanduser("~/Downloads"),
        "&": os.path.expanduser("~/Appdata")
    }


    processed_args = []
    for arg in args:
        new_arg = arg
        for shortcut, full_path in replacements.items():
            if shortcut in new_arg:
                new_arg = new_arg.replace(shortcut, full_path)
        processed_args.append(new_arg)


    if cmd in COMMANDS:
        COMMANDS[cmd](processed_args)
    else:
        print(Fore.RED + "finder_cli command syntax or the command is invalid, please try again" + Style.RESET_ALL)

if __name__ == "__main__":
    while True:
        try:
            parse_command()
        except KeyboardInterrupt:
            print("\nExiting...")
            break