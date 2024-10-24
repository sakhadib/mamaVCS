# command_factory.py

from commands import InitCommand, AddCommand, CommitCommand, StatusCommand, LogCommand, DiffCommand
from commands import RollbackCommand

class CommandFactory:
    """Factory to create command objects based on user input."""

    @staticmethod
    def get_command(command_name, args):
        commands = {
            "shuru": InitCommand,
            "dekho": AddCommand,
            "rakho": CommitCommand,
            "ki_obostha": StatusCommand,
            "itihas": LogCommand,
            "alada_ki": DiffCommand,
            "fire_jao": RollbackCommand,
        }

        if command_name not in commands:
            raise ValueError(f"Unknown command: {command_name}")

        # Handle commands with and without arguments
        command_class = commands[command_name]
        if command_name == "shuru" or command_name == "ki_obostha" or command_name == "itihas":
            return command_class()  # No arguments needed
        else:
            return command_class(args)  # Pass args for commands that need them
