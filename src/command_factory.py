# command_factory.py

from commands import InitCommand, AddCommand, CommitCommand, StatusCommand, LogCommand, DiffCommand
from commands import RollbackCommand, CommitDetailsCommand, PullRepoCommand

class CommandFactory:
    """Factory to create command objects based on user input."""

    @staticmethod
    def get_command(command_name, args):
        """
        Retrieves the appropriate command class based on the provided command name and arguments.
        Args:
            command_name (str): The name of the command to retrieve.
            args (list): The arguments to pass to the command class, if required.
        Returns:
            Command: An instance of the command class corresponding to the command name.
        Raises:
            ValueError: If the command_name is not recognized.
        Commands:
            - "shuru": InitCommand (no arguments)
            - "dekho": AddCommand (requires arguments)
            - "rakho": CommitCommand (requires arguments)
            - "ki_obostha": StatusCommand (no arguments)
            - "itihas": LogCommand (no arguments)
            - "alada_ki": DiffCommand (requires arguments)
            - "fire_jao": RollbackCommand (requires arguments)
        """
        
        
        commands = {
            "shuru": InitCommand,
            "dekho": AddCommand,
            "rakho": CommitCommand,
            "ki_obostha": StatusCommand,
            "itihas": LogCommand,
            "dekhao": CommitDetailsCommand,
            "alada_ki": DiffCommand,
            "fire_jao": RollbackCommand,
            "niye_aso": PullRepoCommand,
        }

        if command_name not in commands:
            raise ValueError(f"Unknown command: {command_name}")

        # Handle commands with and without arguments
        command_class = commands[command_name]
        if command_name == "shuru" or command_name == "ki_obostha" or command_name == "itihas":
            return command_class()  # No arguments needed
        else:
            return command_class(args)  # Pass args for commands that need them

# Hello Mister