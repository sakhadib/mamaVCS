# commands.py

import difflib
import os

from repository import Repository

class InitCommand:
    """Initialize the repository."""
    def execute(self):
        Repository.init()

class AddCommand:
    """Add files to the repository."""
    def __init__(self, args):
        self.filename = args[0] if args else "."

    def execute(self):
        repo = Repository()
        if self.filename == ".":
            repo.add_all()
        else:
            repo.add(self.filename)

class CommitCommand:
    """Commit changes to the repository."""
    def __init__(self, args):
        self.message = args[0] if args else "No message."

    def execute(self):
        repo = Repository()
        repo.commit(self.message)

class StatusCommand:
    """Show the status of the repository."""
    def execute(self):
        repo = Repository()
        repo.status()

class LogCommand:
    """Display the commit history."""
    def execute(self):
        repo = Repository()
        repo.show_log()
        



class DiffCommand:
    """Compare files between commits or with the working directory."""

    def __init__(self, args):
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
        repo = Repository()
        if self.file_to_compare:
            # Compare working file with the last commit
            self.compare_with_last_commit(repo, self.file_to_compare)
        else:
            # Compare two commits
            self.compare_commits(repo, self.commit_id_1, self.commit_id_2)

    def compare_with_last_commit(self, repo, filename):
        """Compare a working file with the last committed version."""
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
        """Compare files between two commits."""
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









# 20241023193207    20241023193831