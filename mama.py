# mama.py

import sys
from command_factory import CommandFactory

def main():
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
