# **Mama VCS**  
A simple version control system (VCS) implemented in Python, allowing users to track changes, commit files, and manage repositories in a simple way.

---

## **Features**
- Initialize a repository in any folder.
- Track changes with `add` and `commit`.
- View the commit history and repository status.
- Compare differences between commits or between a working file and its last committed state.

---

## **Installation Guide**

### **1. Download and Install `mama.exe`**
1. Get the **`mama.exe`** file from the **`dist/`** folder or from a shared link.
2. Place `mama.exe` in a suitable location like:
   ```
   C:\Program Files\mama\
   ```

### **2. Add Mama to System PATH (Windows)**
1. Press **Windows + R** and type:
   ```bash
   sysdm.cpl
   ```
2. Go to **Advanced** → **Environment Variables**.
3. In **User Variables**, find or create a variable called **Path** and click **Edit**.
4. Add the directory containing `mama.exe` (e.g., `C:\Program Files\mama\`).
5. Click **OK** and **restart the terminal** to apply the changes.

---

## **Usage Guide**

Once installed, you can run `mama` commands from any folder in the terminal.

### **1. Initialize a Repository**
```bash
mama shuru
```
- Initializes a new repository in the current folder.

### **2. Add Files to Staging Area**
- **Add a specific file**:
   ```bash
   mama dhoro <filename>
   ```
- **Add all files** in the current directory:
   ```bash
   mama dhoro .
   ```

### **3. Commit Changes**
```bash
mama rakho "Commit message"
```
- Saves the staged files as a new commit with the given message.

### **4. Check Repository Status**
```bash
mama ki_obostha
```
- Displays the current status of the repository, including staged files.

### **5. View Commit History**
```bash
mama itihas
```
- Displays the commit log, showing all previous commits with their details.

### **6. Compare Files**
- **Compare a file with its last committed version**:
   ```bash
   mama alada_ki <filename>
   ```
- **Compare two specific commits**:
   ```bash
   mama alada_ki <commit_id_1> <commit_id_2>
   ```

---

## **Example Workflow**

1. **Initialize the repository:**
   ```bash
   mama shuru
   ```

2. **Add files:**
   ```bash
   mama dhoro example.txt
   mama dhoro .
   ```

3. **Commit the changes:**
   ```bash
   mama rakho "First version"
   ```

4. **Check the status:**
   ```bash
   mama ki_obostha
   ```

5. **View commit history:**
   ```bash
   mama itihas
   ```

6. **Compare changes:**
   ```bash
   mama alada_ki example.txt
   ```

---

## **Troubleshooting**
1. **'mama' is not recognized as a command**:
   - Ensure the directory containing `mama.exe` is added to the **PATH** and restart your terminal.

2. **Permission issues**:
   - Try running the terminal as **Administrator**.

3. **Repository not initialized**:
   - Make sure to run:
     ```bash
     mama shuru
     ```
   - This creates the required `.mama` folder to store your repository data.

---

## **License**
This project is open-source and free to use.
