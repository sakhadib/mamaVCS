# mama.py

import sys
from command_factory import CommandFactory

def main():
    """
    Main function that serves as the entry point for the script.
    This function checks if the required command-line arguments are provided,
    retrieves the command name and arguments, and executes the corresponding command
    using the CommandFactory. If an invalid command is provided, it catches the
    ValueError and prints the error message.
    Usage:
        mama <command> [<args>]
    Raises:
        ValueError: If the command is not found or invalid.
    """
    if len(sys.argv) < 2:
        print("Usage: mama <command> [<args>]")
        return

    command_name = sys.argv[1]
    args = sys.argv[2:]

    try:
        command = CommandFactory.get_command(command_name, args)
        command.execute()
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()


# This is a simple comment