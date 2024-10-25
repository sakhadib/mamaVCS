# commands.py

import difflib
import os
import subprocess
import shutil

from repository import Repository






class InitCommand:
    """
    Class to handle the initialization of a repository.

    Methods:
        execute: Initializes the repository by calling the Repository.init() method.
    """
    def execute(self):
        Repository.init()







class AddCommand:
    """
    AddCommand is a class that represents the 'add' command in a version control system.
    Attributes:
        filename (str): The name of the file to be added. Defaults to "." which indicates all files.
    Methods:
        __init__(args):
            Initializes the AddCommand with the given arguments.
        execute():
            Executes the add command. If the filename is ".", it adds all files to the repository.
            Otherwise, it adds the specified file to the repository.
    """
    
    def __init__(self, args):
        self.filename = args[0] if args else "."

    def execute(self):
        repo = Repository()
        if self.filename == ".":
            repo.add_all()
        else:
            repo.add(self.filename)






class CommitCommand:
    """
    CommitCommand is responsible for committing changes to the repository.
    Attributes:
        message (str): The commit message.
    Methods:
        __init__(args):
            Initializes the CommitCommand with the provided arguments.
        execute():
            Executes the commit command, committing changes to the repository with the specified message.
    """
    """Commit changes to the repository."""






    def __init__(self, args):
        """
        Initializes the command with the given arguments.

        Args:
            args (list): A list of arguments where the first element is expected to be a message.

        Attributes:
            message (str): The message extracted from the arguments or a default message if no arguments are provided.
        """
        self.message = args[0] if args else "No message."






    def execute(self):
        """
        Executes the commit command on the repository.

        This method creates an instance of the `Repository` class and calls its 
        `commit` method with the provided commit message.

        Attributes:
            message (str): The commit message to be used for the commit.

        Raises:
            Exception: If the commit operation fails.
        """
        repo = Repository()
        repo.commit(self.message)












class StatusCommand:
    """
    StatusCommand is a command class that shows the status of the repository.

    Methods:
        execute(): Instantiates a Repository object and calls its status method to display the repository status.
    """



    def execute(self):
        """
        Executes the command by creating a Repository instance and calling its status method.

        This method initializes a new Repository object and invokes its status method to 
        check the current state of the repository.
        """
        repo = Repository()
        repo.status()










class LogCommand:
    """Display the commit history."""
    
    
    def execute(self):
        """
        Executes the command to show the repository log.

        This method creates an instance of the Repository class and calls its
        show_log method to display the log of the repository.
        """
        repo = Repository()
        repo.show_log()
        






class DiffCommand:
    """Compare two commits and display the differences."""

    def __init__(self, args):
        if len(args) != 2:
            raise ValueError("Usage: mama alada_ki <commit_id_1> <commit_id_2>")
        self.commit_id_1 = args[0]
        self.commit_id_2 = args[1]

    def execute(self):
        """Execute the comparison between two commits."""
        repo = Repository()
        repo.compare_commits(self.commit_id_1, self.commit_id_2)












class RollbackCommand:
    """Rollback to a specific commit."""
    def __init__(self, args):
        if not args:
            raise ValueError("Commit ID is required for rollback.")
        self.commit_id = args[0]

    def execute(self):
        """Execute the rollback to the specified commit."""
        repo = Repository()
        repo.rollback(self.commit_id)




class CommitDetailsCommand:
    """
    Command to display details of a specific commit.
    """

    def __init__(self, args):
        if not args:
            raise ValueError("Commit ID is required for this command.")
        self.commit_id = args[0]

    def execute(self):
        """
        Executes the command to show details of a specific commit.
        """
        repo = Repository()
        repo.show_commit_details(self.commit_id)
        
        



class PullRepoCommand:
    """Command to pull the latest files from a GitHub repository."""

    def __init__(self, args):
        if not args:
            raise ValueError("Repository link is required.")
        self.repo_url = args[0]

    def execute(self):
        """Execute the command to pull the latest files."""
        try:
            # Ask the user for a folder name
            folder_name = input("Enter the name of the new folder to store the files: ").strip()
            if not folder_name:
                raise ValueError("Folder name cannot be empty.")

            # Step 1: Clone the repository with depth 1 into a temporary folder
            subprocess.run(
                ["git", "clone", "--depth", "1", self.repo_url, "mama_repo"],
                check=True
            )

            # Step 2: Create the user-specified folder
            os.makedirs(folder_name, exist_ok=True)

            # Step 3: Move the files from mama_repo to the new folder
            for item in os.listdir("mama_repo"):
                shutil.move(os.path.join("mama_repo", item), folder_name)

            # Step 4: Clean up the temporary repository folder
            shutil.rmtree("mama_repo")
            print(f"Files successfully pulled into '{folder_name}', mama.")

        except subprocess.CalledProcessError:
            print("Git cloning failed. Check the repository link.")
        except Exception as e:
            print(f"Error: {e}")