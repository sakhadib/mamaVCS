# repository.py

import os
import shutil
import hashlib
import difflib
from datetime import datetime
import json
from colorama import Fore, Style, init

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
    LOG_FILE = ".mama/log.json"
    HEAD_FILE = ".mama/HEAD"
    TRACK_FILE = ".mama/track.json"






    def __init__(self):
        """
        Initializes the repository.

        Raises:
            Exception: If the repository is not initialized (i.e., the ".mama" directory does not exist).
        """
        if not os.path.exists(".mama"):
            raise Exception("Repository not initialized. Run 'mama shuru'.")
        
        if not os.path.exists(self.LOG_FILE):
            with open(self.LOG_FILE, 'w') as f:
                json.dump([], f)  # Initialize with an empty list








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
        Adds a file to the tracking system.
        This method checks if the specified file exists and computes its hash. If the file is already tracked and 
        unchanged, it skips the addition. Otherwise, it updates the tracking information and adds the file to the index.
        Args:
            filename (str): The name of the file to be added.
        Returns:
            None
        Raises:
            None
        Side Effects:
            - Prints messages to the console regarding the status of the file addition.
            - Updates the tracking information in the tracking file.
            - Appends the filename to the index file.
        """
        
        tracked_files = self.load_tracked_files()

        if not os.path.exists(filename):
            print(f"Ish: {filename} file to khuija pailam na.")
            return

        current_hash = self.hash_file(filename)
        if filename in tracked_files and tracked_files[filename] == current_hash:
            # print(f"{filename} unchanged. Skipping.")
            return

        # Update track.json with the new hash
        tracked_files[filename] = current_hash
        self.save_tracked_files(tracked_files)

        # Add to index
        with open(self.INDEX_FILE, 'a') as f:
            f.write(filename + '\n')
        print(f"Dekhlam {filename}")









    def add_all(self):
        """Stage all modified or new files."""
        for root, _, files in os.walk("."):
            for file in files:
                relative_path = os.path.relpath(os.path.join(root, file), ".")
                if not self.is_excluded(relative_path, self.load_exclusions()):
                    self.add(relative_path)






    def load_tracked_files(self):
        """Load file hashes from track.json."""
        if os.path.exists(self.TRACK_FILE):
            with open(self.TRACK_FILE, 'r') as f:
                return json.load(f)
        return {}
    
    
    
    
    

    def save_tracked_files(self, tracked_files):
        """Save the complete tracked file list with hashes to track.json."""
        with open(self.TRACK_FILE, 'w') as f:
            json.dump(tracked_files, f, indent=4)






    def load_tracked_files(self):
        """Load the tracked files and their hashes from track.json."""
        if os.path.exists(self.TRACK_FILE):
            with open(self.TRACK_FILE, 'r') as f:
                return json.load(f)
        return {}
    
    
    
    
    
    


    def is_modified_or_new(self, filename, commit_id):
        """
        Check if a file is new or modified compared to the last commit.
        Args:
            filename (str): The name of the file to check.
            commit_id (str): The ID of the last commit.
        Returns:
            bool: True if the file is new or modified, False otherwise.
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
        """Commit staged files and ensure all tracked files are retained in track.json."""
        staged_files = self.get_staged_files()
        tracked_files = self.load_tracked_files()

        # Check if any staged file was modified after staging
        modified_files = [
            f for f in staged_files if tracked_files.get(f) != self.hash_file(f)
        ]

        if modified_files:
            print("Warning! The following files were modified after staging:")
            for file in modified_files:
                print(f"  - {file}")
            print("Please re-stage them before committing.")
            return

        # Proceed with commit
        commit_id = datetime.now().strftime("%Y%m%d%H%M%S")
        commit_folder = os.path.join(self.COMMITS_DIR, commit_id)
        os.mkdir(commit_folder)

        for filename in staged_files:
            shutil.copy2(filename, commit_folder)

        # Log the commit with file names and hashes
        self.log_commit(commit_id, message, staged_files)

        # Update tracked files: Keep old entries and add new/modified ones
        for file in staged_files:
            tracked_files[file] = self.hash_file(file)

        # Save updated tracked files to track.json
        self.save_tracked_files(tracked_files)

        # Clear the index
        self.clear_index()
        print(f"Rekhe disi mama {commit_id}. Kono pera nai.")












    def log_commit(self, commit_id, message, files):
        """Log the commit details with both file names and their hash values to log.json."""
        log_data = self.load_commit_log()

        # Prepare log entry: List of dictionaries with file name and hash
        file_entries = [
            {"file_name": file, "hash": self.hash_file(file)} for file in files
        ]

        log_entry = {
            "commit_id": commit_id,
            "message": message,
            "files": file_entries,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        log_data.append(log_entry)

        with open(self.LOG_FILE, 'w') as f:
            json.dump(log_data, f, indent=4)





    
    
    
    def load_commit_log(self):
        """Load the commit log from log.json. Return an empty list if the file is empty or missing."""
        if os.path.exists(self.LOG_FILE):
            try:
                with open(self.LOG_FILE, 'r') as f:
                    return json.load(f) or []  # Ensure it returns an empty list if the file is empty
            except json.JSONDecodeError:
                print("Log file is corrupted. Initializing a new log.")
                return []
        return []





    def get_staged_files(self):
        """Retrieve the list of staged files from the index."""
        if not os.path.exists(self.INDEX_FILE):
            return []
        with open(self.INDEX_FILE, 'r') as f:
            return [line.strip() for line in f if line.strip()]








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
        Displays the commit history from log.json in a colorful and clean format.
        If there are no commits, it will notify the user.
        """
        log_data = self.load_commit_log()

        if not log_data:
            print(Fore.RED + "Kono commit nai mama. Kichu commit korun agey!")
            return

        print(Fore.CYAN + "\n========== Mama Itihas ==========\n")
        
        for entry in log_data:
            print(Fore.GREEN + f"Commit ID   : {Fore.WHITE}{entry['commit_id']}")
            print(Fore.GREEN + f"Message     : {Fore.WHITE}{entry['message']}")
            print(Fore.GREEN + f"Date & Time : {Fore.WHITE}{entry['timestamp']}")
            print(Fore.YELLOW + "-" * 30)

        print(Style.RESET_ALL + Fore.WHITE + "\nEi hoilo apnar repository er itihas.\n")





    def show_commit_details(self, commit_id):
        """
        Displays detailed information for a specific commit based on the given ID.
        """
        log_data = self.load_commit_log()

        # Find the specific commit
        commit = next((entry for entry in log_data if entry["commit_id"] == commit_id), None)
        if not commit:
            print(Fore.RED + f"Commit ID '{commit_id}' pawa jai nai!")
            return

        # Display the details of the specific commit
        print(Fore.CYAN + "\n========== Commit Details ==========\n")
        print(Fore.GREEN + f"Commit ID   : {Fore.WHITE}{commit['commit_id']}")
        print(Fore.GREEN + f"Message     : {Fore.WHITE}{commit['message']}")
        print(Fore.GREEN + f"Date & Time : {Fore.WHITE}{commit['timestamp']}")
        print(Fore.GREEN + "Files:")
        for file in commit["files"]:
            print(Fore.WHITE + f"  - {file['file_name']}")
        print(Style.RESET_ALL)





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
        """Rollback to a specific commit by restoring files and removing commit history."""
        if not os.path.exists(os.path.join(self.COMMITS_DIR, commit_id)):
            print(f"Commit {commit_id} not found.")
            return

        # Step 1: Delete files created after the target commit
        self.delete_files_after_commit(commit_id)

        # Step 2: Restore files to their correct paths from relevant commits
        self.restore_files_to_commit(commit_id)

        # Step 3: Verify restored files
        self.verify_restored_files()

        # Step 4: Delete commit history after the target commit
        self.delete_commit_history_after(commit_id)

        # Step 5: Log rollback information
        self.log_rollback(commit_id)

        print(f"Successfully rolled back to commit {commit_id}.")









    def delete_files_after_commit(self, commit_id):
        """Delete files created after the target commit."""
        all_commits = sorted(os.listdir(self.COMMITS_DIR))
        commits_to_check = all_commits[all_commits.index(commit_id) + 1:]

        files_to_delete = set()
        for commit in commits_to_check:
            commit_folder = os.path.join(self.COMMITS_DIR, commit)
            files_to_delete.update(os.listdir(commit_folder))

        for file in files_to_delete:
            if os.path.exists(file):
                os.remove(file)
                print(f"Deleted: {file}")

        # Remove these files from track.json
        tracked_files = self.load_tracked_files()
        for file in files_to_delete:
            tracked_files.pop(file, None)
        self.save_tracked_files(tracked_files)









    def restore_files_to_commit(self, commit_id):
        """Restore files to their original paths based on log.json for the specified commit."""
        all_commits = sorted(os.listdir(self.COMMITS_DIR))
        relevant_commits = all_commits[: all_commits.index(commit_id) + 1]

        # Load log data to map files to their correct paths
        log_data = self.load_commit_log()
        restored_files = {}

        # Iterate over relevant commits in reverse to restore the latest version <= commit_id
        for commit in reversed(relevant_commits):
            commit_entry = next((entry for entry in log_data if entry["commit_id"] == commit), None)
            if not commit_entry:
                continue  # Skip if no matching log entry found

            for file_info in commit_entry["files"]:
                file_name = file_info["file_name"]  # This includes the original path
                commit_folder = os.path.join(self.COMMITS_DIR, commit)
                source_path = os.path.join(commit_folder, os.path.basename(file_name))  # File is stored without structure

                # Ensure the original path is recreated
                target_path = os.path.join(".", file_name)  # Restore to the original path from log.json
                target_dir = os.path.dirname(target_path)
                os.makedirs(target_dir, exist_ok=True)

                # Copy the file only if it hasn't been restored yet
                if file_name not in restored_files:
                    shutil.copy2(source_path, target_path)
                    restored_files[file_name] = True
                    print(f"Restored: {file_name} to {target_path} from commit {commit}")










    def verify_restored_files(self):
        """Ensure all restored files match their expected hashes."""
        tracked_files = self.load_tracked_files()
        for file, expected_hash in tracked_files.items():
            if os.path.exists(file):
                current_hash = self.hash_file(file)
                if current_hash != expected_hash:
                    print(f"Hash mismatch for {file}! Expected: {expected_hash}, Found: {current_hash}")







    def delete_commit_history_after(self, commit_id):
        """Delete commit history beyond the target commit."""
        all_commits = sorted(os.listdir(self.COMMITS_DIR))
        commits_to_delete = all_commits[all_commits.index(commit_id) + 1:]

        for commit in commits_to_delete:
            shutil.rmtree(os.path.join(self.COMMITS_DIR, commit))
            print(f"Deleted commit history: {commit}")

        # Update log.json to reflect the rollback
        log_data = self.load_commit_log()
        updated_log = [entry for entry in log_data if entry["commit_id"] <= commit_id]
        with open(self.LOG_FILE, 'w') as f:
            json.dump(updated_log, f, indent=4)








    def log_rollback(self, commit_id):
        """Log rollback information in rollback.json."""
        rollback_data = {
            "rollback_to": commit_id,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        with open(".mama/rollback.json", 'w') as f:
            json.dump(rollback_data, f, indent=4)








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
        """Print the line-by-line diff between two files."""
        with open(file1, 'r') as f1, open(file2, 'r') as f2:
            diff = difflib.unified_diff(
                f1.readlines(), f2.readlines(),
                fromfile=file1, tofile=file2
            )
            print(''.join(diff))









    def compare_commits(self, commit1, commit2):
        """
        Compare files between two commits and display detailed differences.
        Args:
            commit1 (str): The identifier for the first commit.
            commit2 (str): The identifier for the second commit.
        """
        commit_folder1 = os.path.join(self.COMMITS_DIR, commit1)
        commit_folder2 = os.path.join(self.COMMITS_DIR, commit2)

        if not os.path.exists(commit_folder1) or not os.path.exists(commit_folder2):
            print(f"Commit {commit1} or {commit2} er information nai, mama.")
            return

        files1 = set(os.listdir(commit_folder1))
        files2 = set(os.listdir(commit_folder2))

        # Identify new, deleted, and modified files
        new_files = files2 - files1
        deleted_files = {f for f in files1 - files2 if not os.path.exists(f)}
        common_files = files1 & files2

        print(Fore.CYAN + "\nNew Files Added:")
        for file in new_files:
            print(Fore.GREEN + f"  - {file}")

        print(Fore.CYAN + "\nFiles Deleted:")
        for file in deleted_files:
            print(Fore.RED + f"  - {file}")

        print(Fore.CYAN + "\nModified Files:")
        for file in common_files:
            file1 = os.path.join(commit_folder1, file)
            file2 = os.path.join(commit_folder2, file)

            if not self.files_are_equal(file1, file2):
                print(Fore.YELLOW + f"\nChanges in {file}:")
                self.print_diff(file1, file2)

        print(Style.RESET_ALL)





    def files_are_equal(self, file1, file2):
        """Check if two files are identical by comparing their hashes."""
        return self.hash_file(file1) == self.hash_file(file2)
    
    
    
    
    
    