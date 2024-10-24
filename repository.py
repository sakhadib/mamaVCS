# repository.py

import os
import shutil
import hashlib
import difflib
from datetime import datetime

class Repository:
    """
    Repository class for managing a simple version control system.
    Attributes:
        EXCLUDED_DIRS (set): Directories to exclude from tracking.
        COMMITS_DIR (str): Directory to store commits.
        INDEX_FILE (str): File to store the index of staged files.
        LOG_FILE (str): File to store the commit log.
        HEAD_FILE (str): File to store the current HEAD commit.
    Methods:
        __init__(): Initialize the repository instance.
        init(): Initialize the repository.
        add(filename): Add a single file to the index.
        add_all(): Stage only modified or new files.
        is_modified_or_new(filename, commit_id): Check if a file is new or modified compared to the last commit.
        stage_new_files(): Stage all files as new when no prior commits exist.
        is_tracked(filename): Check if a file is already tracked.
        load_exclusions(): Load excluded files.
        is_excluded(path, exclusions): Check if a path matches any excluded directories.
        commit(message): Commit the staged files and show the summary of changes.
        get_last_commit(): Get the previous commit ID.
        show_commit_summary(new_commit_id, new_files): Show the summary of additions and deletions compared to the last commit.
        clear_index(): Clear the staging area by emptying the index file.
        hash_file(filename): Generate a SHA-256 hash of the file's contents.
        show_log(): Display the commit history from the log file.
        status(): Show the status of the repository.
        rollback(commit_id): Rollback to a specific commit.
        rollback_to_previous(): Rollback to the previous commit.
        compare_with_commit(commit_id): Compare working directory with the given commit.
        compare_latest_with_previous(): Compare the latest and previous commits.
        print_diff(file1, file2): Print the unified diff between two files.
        compare_commits(commit1, commit2): Compare files between two commits.
    """
    
    
    
    
    
    EXCLUDED_DIRS = {"venv/", "mama/", ".mama/", "node_modules/"}
    COMMITS_DIR = ".mama/commits"
    INDEX_FILE = ".mama/index.txt"
    LOG_FILE = ".mama/log.txt"
    HEAD_FILE = ".mama/HEAD"






    def __init__(self):
        """
        Initializes the repository.

        Raises:
            Exception: If the repository is not initialized (i.e., the ".mama" directory does not exist).
        """
        if not os.path.exists(".mama"):
            raise Exception("Repository not initialized. Run 'mama shuru'.")







    @staticmethod
    def init():
        """
            Initializes a new repository.
            This method checks if a repository is already initialized by looking for the 
            presence of a ".mama" directory. If the directory exists, it prints a message 
            indicating that the repository is already initialized and returns. Otherwise, 
            it creates the necessary directories and files for the repository and prints 
            a message indicating that the repository has been successfully initialized.
        Raises:
            OSError: If there is an error creating the directories or files.
        """
        if os.path.exists(".mama"):
            print("Repository already initialized.")
            return
        os.makedirs(Repository.COMMITS_DIR)
        open(Repository.INDEX_FILE, 'w').close()
        open(Repository.LOG_FILE, 'w').close()
        print("Repository toiri hoise. cholen kam shuru kori! \n\n")







    def add(self, filename):
        """
        Add a single file to the index.

        Args:
            filename (str): The name of the file to add to the index.

        Returns:
            None

        Prints:
            A message indicating whether the file was added, already tracked, or not found.
        """
        """Add a single file to the index."""
        if not os.path.exists(filename):
            print(f"Ish: {filename} file to khuija pailam na mama repository te.")
            return
        if self.is_tracked(filename):
            print(f"{filename} file ta to agei dekhsi ami, mama")
            return
        with open(self.INDEX_FILE, 'a') as f:
            f.write(filename + '\n')
        print(f"Dekhlam {filename}")








    def add_all(self):
        """
        Stage only modified or new files for the next commit.
        This method stages files that have been modified or newly created since the last commit.
        If there is no previous commit, it stages all new files. It excludes files based on
        exclusion rules defined in the repository.
        Steps:
        1. Retrieve the last commit.
        2. If no last commit exists, stage all new files.
        3. Walk through the working directory and compare each file with the last commit.
        4. Stage files that are either modified or new, excluding files based on exclusion rules.
        Note:
        - The method prints a message if there is no previous commit.
        - It uses helper methods `get_last_commit`, `stage_new_files`, `is_excluded`, 
        `load_exclusions`, and `is_modified_or_new` to perform its operations.
        """
        last_commit = self.get_last_commit()
        if not last_commit:
            print("Pechone kichu nai mama, sob new dhorte hobe.")
            self.stage_new_files()
            return

        # Compare working directory files with the latest commit
        for root, _, files in os.walk("."):
            for file in files:
                filepath = os.path.join(root, file)
                relative_path = os.path.relpath(filepath, ".")
                if not self.is_excluded(relative_path, self.load_exclusions()):
                    if self.is_modified_or_new(relative_path, last_commit):
                        self.add(relative_path)  # Stage only modified or new files








    def is_modified_or_new(self, filename, commit_id):
        """
        Check if a file is new or modified compared to the last commit.
        Args:
            filename (str): The name of the file to check.
            commit_id (str): The ID of the commit to compare against.
        Returns:
            bool: True if the file is new or has been modified, False otherwise.
        """

        commit_file = os.path.join(self.COMMITS_DIR, commit_id, filename)
        if not os.path.exists(commit_file):
            return True  # New file

        # Check if the content has changed
        return self.hash_file(filename) != self.hash_file(commit_file)







    def stage_new_files(self):
        """
        Stage all files as new when no prior commits exist.

        This method walks through the current directory and stages all files
        that are not excluded based on the exclusion rules. It uses the 
        `os.walk` function to traverse the directory tree and stages each 
        file by calling the `add` method with the relative path of the file.

        Exclusion rules are loaded using the `load_exclusions` method and 
        checked with the `is_excluded` method.

        Returns:
            None
        """

        for root, _, files in os.walk("."):
            for file in files:
                filepath = os.path.join(root, file)
                relative_path = os.path.relpath(filepath, ".")
                if not self.is_excluded(relative_path, self.load_exclusions()):
                    self.add(relative_path)








    def is_tracked(self, filename):
        """
        Check if a file is tracked in the repository.
        Args:
            filename (str): The name of the file to check.
        Returns:
            bool: True if the file is tracked, False otherwise.
        """

        if not os.path.exists(self.INDEX_FILE):
            return False
        with open(self.INDEX_FILE, 'r') as f:
            tracked_files = f.read().splitlines()
        return filename in tracked_files







    def load_exclusions(self):
        """
        Load exclusions from a predefined set and an optional file.
        This method initializes a set of exclusions from the `EXCLUDED_DIRS` attribute.
        If a file named ".mama_bad_dao" exists in the current directory, it reads the file
        and adds each non-empty, stripped line to the exclusions set.
        Returns:
            set: A set containing the combined exclusions from `EXCLUDED_DIRS` and the ".mama_bad_dao" file.
        """

        exclusions = set(self.EXCLUDED_DIRS)
        if os.path.exists(".mama_bad_dao"):
            with open(".mama_bad_dao", 'r') as f:
                exclusions.update(line.strip() for line in f if line.strip())
        return exclusions







    def is_excluded(self, path, exclusions):
        """
        Determines if a given path is excluded based on a list of exclusion paths.
        Args:
            path (str): The path to check.
            exclusions (list of str): A list of paths to exclude.
        Returns:
            bool: True if the path is excluded, False otherwise.
        """

        abs_path = os.path.abspath(path)
        return any(abs_path.startswith(os.path.abspath(ex)) for ex in exclusions)








    def commit(self, message):
        """
        Commits the current changes in the repository with a given message.
        This method performs the following steps:
        1. Reads the list of files from the index file.
        2. If there are no files to commit, it prints a message and returns.
        3. Creates a unique commit ID based on the current timestamp.
        4. Creates a new directory for the commit using the commit ID.
        5. Copies the files from the index to the commit directory and computes their hashes.
        6. Logs the commit details, including the commit ID, message, filenames, and their hashes.
        7. Compares the current commit with the last commit and shows a summary of changes.
        8. Clears the index after a successful commit.
        Args:
            message (str): The commit message describing the changes.
        """

        with open(self.INDEX_FILE, 'r') as f:
            files = [line.strip() for line in f if line.strip()]

        if not files:
            print("Rakhar jonno notun kichu nai to mama repository te.")
            return

        # Create a unique commit ID based on timestamp
        commit_id = datetime.now().strftime("%Y%m%d%H%M%S")
        commit_folder = os.path.join(self.COMMITS_DIR, commit_id)
        os.mkdir(commit_folder)

        # Copy files to the commit folder and compute their hashes
        for filename in files:
            if os.path.exists(filename):
                shutil.copy2(filename, commit_folder)
                file_hash = self.hash_file(filename)
                print(f"Rakhtesi mama {filename} file ta. Hash hoilo {file_hash}")

        # Log the commit details
        with open(self.LOG_FILE, 'a') as f:
            f.write(f"Commit {commit_id}: {message}\n")
            for filename in files:
                file_hash = self.hash_file(filename)
                f.write(f"  {filename}: {file_hash}\n")
            f.write("\n")

        # Compare with the last commit and show the summary of changes
        self.show_commit_summary(commit_id, files)

        # Clear the index after a successful commit
        self.clear_index()
        print(f"Rekhe disi mama {commit_id}. kono pera nai")







    def get_last_commit(self):
        """
        Retrieve the previous commit ID from the commits directory.
        This method sorts the commit IDs in the commits directory in descending order
        and returns the second most recent commit ID. If there are no commits, it returns None.
        Returns:
            str or None: The previous commit ID if available, otherwise None.
        """
        commits = sorted(os.listdir(self.COMMITS_DIR), reverse=True)

        # Ensure we don't return the current commit, only previous ones
        return commits[1] if commits else None








    def show_commit_summary(self, new_commit_id, new_files):
        """
        Display a summary of the changes between the last commit and the new commit.
        Args:
            new_commit_id (str): The identifier for the new commit.
            new_files (list): A list of file names included in the new commit.
        Returns:
            None
        """

        last_commit_id = self.get_last_commit()

        if not last_commit_id:
            print(f"{len(new_files)} additions, 0 deletions.")
            return

        # Build the path to the last commit folder correctly
        last_commit_folder = last_commit_id

        new_files_set = set(new_files)
        previous_files_set = set(os.listdir(last_commit_folder))

        # Calculate additions and deletions
        additions = new_files_set - previous_files_set
        deletions = previous_files_set - new_files_set

        # print(f"{len(additions)} additions, {len(deletions)} deletions.")








    def clear_index(self):
        """
        Clears the contents of the index file.
        This method opens the index file in write mode and writes an empty string to it,
        effectively clearing any existing content in the file.
        """

        with open(self.INDEX_FILE, 'w') as f:
            f.write("")  # Empty the index
        # print("Staging area cleared.")









    @staticmethod
    def hash_file(filename):
        """
        Computes the SHA-256 hash of a file.
        Args:
            filename (str): The path to the file to be hashed.
        Returns:
            str: The SHA-256 hash of the file in hexadecimal format.
        """

        sha256 = hashlib.sha256()
        with open(filename, 'rb') as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()









    def get_last_commit(self):
        """
        Retrieve the most recent commit from the commits directory.
        This method sorts the list of commit files in the commits directory in 
        descending order and returns the path to the latest commit file. If the 
        commits directory is empty, it returns None.
        Returns:
            str or None: The path to the most recent commit file, or None if the 
            commits directory is empty.
        """

        commits = sorted(os.listdir(self.COMMITS_DIR), reverse=True)
        return os.path.join(self.COMMITS_DIR, commits[0]) if commits else None








    def show_log(self):
        """
        Displays the log content of the repository.
        This method checks if the log file exists. If it does not exist, it prints a message indicating that there is no log.
        If the log file exists but is empty or contains only the header "Commit Log:", it prints a message indicating that there is no log content.
        Otherwise, it prints the log content.
        Returns:
            None
        """

        if not os.path.exists(self.LOG_FILE):
            print("Age kichu rakhte bolen nai to mama")
            return

        with open(self.LOG_FILE, 'r') as f:
            log_content = f.read()

        if log_content.strip() == "Commit Log:":
            print("Age kichu rakhte bolen nai to mama")
        else:
            print("Ei hoilo apnar itihas mama repository te:")
            print(log_content)








    def status(self):
        """
        Displays the status of the repository by checking the INDEX_FILE.
        If the INDEX_FILE does not exist or is empty, it prints a message indicating that there are no staged files.
        Otherwise, it prints the list of staged files and the total count of these files.
        Messages are printed in Bengali language.
        Returns:
            None
        """
        
        if not os.path.exists(self.INDEX_FILE):
            print("Age kichu rakhte bolen nai to mama")
            return

        with open(self.INDEX_FILE, 'r') as f:
            staged_files = f.read().splitlines()

        if not staged_files:
            print("Age kichu rakhte bolen nai to mama")
            return

        print("Ei hoilo apnar repository mama ki obostha:")
        for file in staged_files:
            print(f"  {file} (rakha ache)")
        print(f"Total {len(staged_files)} ta file rakha ache mama repository te.")









    def rollback(self, commit_id):
        """
        Rollback the repository to a specified commit.
        This method restores the files from the specified commit folder back to the working directory.
        Args:
            commit_id (str): The ID of the commit to rollback to.
        Returns:
            None
        Prints:
            A message indicating whether the commit was found and the files were restored.
        """

        commit_folder = os.path.join(self.COMMITS_DIR, commit_id)
        
        if not os.path.exists(commit_folder):
            print(f"Commit {commit_id} er information pailam na mama.")
            return

        # Restore the files from the specified commit
        for filename in os.listdir(commit_folder):
            commit_file = os.path.join(commit_folder, filename)
            shutil.copy2(commit_file, filename)  # Copy file back to working directory

        print(f"Commit {commit_id} er file gulo restore korsi, mama.")









    def rollback_to_previous(self):
        """
        Rollback the repository to the previous commit.
        This method retrieves the list of commits in the repository, sorted in reverse order
        (latest commit first). If there are fewer than two commits, it prints a message indicating
        that there are no previous commits to rollback to. Otherwise, it identifies the second
        latest commit and rolls back the repository to that commit.
        Prints:
            A message indicating whether the rollback was successful or if there are no previous commits.
        """

        commits = sorted(os.listdir(self.COMMITS_DIR), reverse=True)
        if len(commits) < 2:
            print("Pechone jawar commit nai mama.")
            return

        previous_commit = commits[1]  # Second latest commit
        self.rollback(previous_commit)
        print(f"Pechone giya {previous_commit} commit ta restore korsi, mama.")








    def compare_with_commit(self, commit_id):
        """
        Compare the current state of files with a specified commit.
        Args:
            commit_id (str): The ID of the commit to compare against.
        Returns:
            None
        Prints:
            - A message if the specified commit does not exist.
            - The differences between the current files and the files in the specified commit.
            - A message if a file from the commit does not exist in the current state.
        """

        commit_folder = os.path.join(self.COMMITS_DIR, commit_id)
        if not os.path.exists(commit_folder):
            print(f"Commit {commit_id} nai mama.")
            return

        for filename in os.listdir(commit_folder):
            commit_file = os.path.join(commit_folder, filename)
            if os.path.exists(filename):
                self.print_diff(commit_file, filename)
            else:
                print(f"{filename} er itihas nai.")








    def compare_latest_with_previous(self):
        """
        Compare the latest and previous commits.
        This method retrieves the list of commits from the COMMITS_DIR directory,
        sorts them in reverse order (latest first), and compares the two most recent commits.
        If there are fewer than two commits, it prints a message indicating that 
        there are not enough commits to compare.
        Returns:
            None
        """

        commits = sorted(os.listdir(self.COMMITS_DIR), reverse=True)
        if len(commits) < 2:
            print("Compare korar jonno komse mama.")
            return

        self.compare_commits(commits[0], commits[1])








    def print_diff(self, file1, file2):
        """
        Print the unified diff between two files.
        Args:
            file1 (str): The path to the first file.
            file2 (str): The path to the second file.
        Returns:
            None
        """

        with open(file1, 'r') as f1, open(file2, 'r') as f2:
            diff = difflib.unified_diff(
                f1.readlines(), f2.readlines(),
                fromfile=file1, tofile=file2
            )
            print(''.join(diff))









    def compare_commits(self, commit1, commit2):
        """
        Compare files between two commits.
        Args:
            commit1 (str): The identifier for the first commit.
            commit2 (str): The identifier for the second commit.
        Returns:
            None
        Prints:
            - A message if either commit does not exist.
            - A message indicating which files are unique to each commit.
            - The differences between files that exist in both commits.
        """

        commit_folder1 = os.path.join(self.COMMITS_DIR, commit1)
        commit_folder2 = os.path.join(self.COMMITS_DIR, commit2)

        if not os.path.exists(commit_folder1) or not os.path.exists(commit_folder2):
            print(f"Commit {commit1} or {commit2} er information nai, mama.")
            return

        files1 = set(os.listdir(commit_folder1))
        files2 = set(os.listdir(commit_folder2))
        all_files = files1 | files2  # Union of both sets

        for file in all_files:
            file1 = os.path.join(commit_folder1, file)
            file2 = os.path.join(commit_folder2, file)

            if not os.path.exists(file1):
                print(f"{file} only found in {commit2}.")
            elif not os.path.exists(file2):
                print(f"{file} only found in {commit1}.")
            else:
                self.print_diff(file1, file2)
