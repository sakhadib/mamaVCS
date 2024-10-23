# repository.py

import os
import shutil
import hashlib
from datetime import datetime

class Repository:
    EXCLUDED_DIRS = {"venv/", "mama/", ".mama/", "node_modules/"}
    COMMITS_DIR = ".mama/commits"
    INDEX_FILE = ".mama/index.txt"
    LOG_FILE = ".mama/log.txt"
    HEAD_FILE = ".mama/HEAD"

    def __init__(self):
        if not os.path.exists(".mama"):
            raise Exception("Repository not initialized. Run 'mama shuru'.")

    @staticmethod
    def init():
        """Initialize the repository."""
        if os.path.exists(".mama"):
            print("Repository already initialized.")
            return
        os.makedirs(Repository.COMMITS_DIR)
        open(Repository.INDEX_FILE, 'w').close()
        open(Repository.LOG_FILE, 'w').close()
        print("Repository toiri hoise. cholen kam shuru kori! \n\n")

    def add(self, filename):
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
        """Add all untracked files."""
        exclusions = self.load_exclusions()
        for root, _, files in os.walk("."):
            for file in files:
                filepath = os.path.join(root, file)
                relative_path = os.path.relpath(filepath, ".")
                if self.is_excluded(relative_path, exclusions):
                    continue
                if not self.is_tracked(relative_path):
                    self.add(relative_path)

    def is_tracked(self, filename):
        """Check if a file is already tracked."""
        if not os.path.exists(self.INDEX_FILE):
            return False
        with open(self.INDEX_FILE, 'r') as f:
            tracked_files = f.read().splitlines()
        return filename in tracked_files

    def load_exclusions(self):
        """Load excluded files."""
        exclusions = set(self.EXCLUDED_DIRS)
        if os.path.exists(".mama_bad_dao"):
            with open(".mama_bad_dao", 'r') as f:
                exclusions.update(line.strip() for line in f if line.strip())
        return exclusions

    def is_excluded(self, path, exclusions):
        """Check if a path matches any excluded directories."""
        abs_path = os.path.abspath(path)
        return any(abs_path.startswith(os.path.abspath(ex)) for ex in exclusions)

    def commit(self, message):
        """Commit the staged files and show the summary of changes."""
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
        """Get the previous commit ID."""
        commits = sorted(os.listdir(self.COMMITS_DIR), reverse=True)

        # Ensure we don't return the current commit, only previous ones
        return commits[1] if commits else None
    
    
    
    def show_commit_summary(self, new_commit_id, new_files):
        """Show the summary of additions and deletions compared to the last commit."""
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
        """Clear the staging area by emptying the index file."""
        with open(self.INDEX_FILE, 'w') as f:
            f.write("")  # Empty the index
        # print("Staging area cleared.")
        
        

    @staticmethod
    def hash_file(filename):
        """Generate a SHA-256 hash of the file's contents."""
        sha256 = hashlib.sha256()
        with open(filename, 'rb') as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()

    def get_last_commit(self):
        """Get the last commit folder."""
        commits = sorted(os.listdir(self.COMMITS_DIR), reverse=True)
        return os.path.join(self.COMMITS_DIR, commits[0]) if commits else None
    
    def show_log(self):
        """Display the commit history from the log file."""
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
        """Show the status of the repository."""
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