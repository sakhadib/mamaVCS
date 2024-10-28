# mama/__init__.py

# Import relevant modules or functions for easy access
from .commands import InitCommand, AddCommand, CommitCommand, StatusCommand, LogCommand, DiffCommand, RollbackCommand, CommitDetailsCommand, PullRepoCommand
from .repository import Repository
from .command_factory import CommandFactory

# Define what gets imported when someone does `from mama import *`
__all__ = [
    "InitCommand",
    "AddCommand",
    "CommitCommand",
    "Repository",
    "CommandFactory",
    "StatusCommand",
    "LogCommand",
    "DiffCommand",
    "RollbackCommand",
    "CommitDetailsCommand",
    "PullRepoCommand"
]
