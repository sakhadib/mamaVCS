# commands.py

import difflib
import os

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
    """Compare files between commits or with the working directory."""




    def __init__(self, args):
        """
        Initializes the command with the given arguments.

        Args:
            args (list): A list of arguments. It can either be:
                - A single argument representing the file to compare with the last commit.
                - Two arguments representing the commit IDs to compare.

        Raises:
            ValueError: If the number of arguments is not 1 or 2.
        """
        if len(args) == 1:
            self.file_to_compare = args[0]  # Compare working file with the last commit
            self.commit_id = None
        elif len(args) == 2:
            self.commit_id_1 = args[0]
            self.commit_id_2 = args[1]
            self.file_to_compare = None
        else:
            raise ValueError("Usage: mama diff <file> | <commit1> <commit2>")






    def execute(self):
        """
        Executes the comparison of commits based on the provided arguments.
        Depending on the number of arguments passed, this method performs different types of comparisons:
        - If two arguments are provided, it compares two specific commits.
        - If one argument is provided, it compares the working directory with a specific commit.
        - If no arguments are provided, it compares the latest commit with the previous commit.
        Args:
            None (uses self.args to determine the comparison type)
        Raises:
            ValueError: If the number of arguments is not 0, 1, or 2.
        """
        repo = Repository()

        if len(self.args) == 2:
            # Compare two specific commits
            repo.compare_commits(self.args[0], self.args[1])
        elif len(self.args) == 1:
            # Compare working directory with a specific commit
            repo.compare_with_commit(self.args[0])
        else:
            # Compare latest and previous commits
            repo.compare_latest_with_previous()






    def compare_with_last_commit(self, repo, filename):
        """
        Compare the specified file with its version in the last commit.
        Args:
            repo: The repository object that provides access to the commit history.
            filename: The name of the file to compare.
        Returns:
            None. Prints the differences between the current file and the file in the last commit.
            If the last commit or the file in the last commit does not exist, prints an appropriate message.
        """

        last_commit = repo.get_last_commit()
        if not last_commit:
            print("Ager kichu paitesi na mama sorry")
            return

        commit_file = os.path.join(last_commit, filename)
        if not os.path.exists(commit_file):
            print(f"Eije file {filename} . Etar to mama itihas nai amar kache")
            return

        with open(commit_file, 'r') as f1, open(filename, 'r') as f2:
            diff = difflib.unified_diff(
                f1.readlines(), f2.readlines(),
                fromfile=f'Commit: {last_commit}/{filename}',
                tofile=f'Working: {filename}'
            )
            print(''.join(diff))






    def compare_commits(self, repo, commit1, commit2):
        """
        Compare the differences between two commits in a repository.
        Args:
            repo (Repository): The repository object.
            commit1 (str): The identifier of the first commit.
            commit2 (str): The identifier of the second commit.
        Returns:
            None
        Prints:
            - A message if either of the commits does not exist.
            - A message indicating which files were added or removed between the commits.
            - The unified diff of the files that exist in both commits but have differences.
        """
        
        commit_folder1 = os.path.join(Repository.COMMITS_DIR, commit1)
        commit_folder2 = os.path.join(Repository.COMMITS_DIR, commit2)

        if not os.path.exists(commit_folder1) or not os.path.exists(commit_folder2):
            print("ei commit gulo mama itihas nai")
            return

        files1 = set(os.listdir(commit_folder1))
        files2 = set(os.listdir(commit_folder2))
        all_files = files1 | files2  # Union of both sets

        for file in all_files:
            file1 = os.path.join(commit_folder1, file)
            file2 = os.path.join(commit_folder2, file)

            if not os.path.exists(file1):
                print(f"{file} rakhsi {commit2} ekhane.")
                continue
            elif not os.path.exists(file2):
                print(f"{file} falay disi {commit2} ekhan theke.")
                continue

            with open(file1, 'r') as f1, open(file2, 'r') as f2:
                diff = difflib.unified_diff(
                    f1.readlines(), f2.readlines(),
                    fromfile=f'{commit1}/{file}',
                    tofile=f'{commit2}/{file}'
                )
                print(''.join(diff))



















class RollbackCommand:
    """Rollback to a specific or the previous commit."""
    def __init__(self, args):
        self.commit_id = args[0] if args else None


    def execute(self):
        """
        Executes the rollback operation on the repository.

        If a specific commit ID is provided, the repository will be rolled back to that commit.
        Otherwise, the repository will be rolled back to the previous commit.

        Attributes:
            commit_id (str): The ID of the commit to roll back to. If None, the repository will roll back to the previous commit.
        """
        repo = Repository()
        if self.commit_id:
            repo.rollback(self.commit_id)
        else:
            repo.rollback_to_previous()






# 20241023193207    20241023193831