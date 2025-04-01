Copyright (c) 2025 nameisname  
This software is licensed under the GNU General Public License v3.0.

# Process Management Task System

## Project Objective
Design a process-centric task management system to address issues such as unreasonable deadlines and working memory limitations in task management. By performing CRUD operations on processes, the system helps users manage tasks more effectively.

## Key Features
- **Process Management**:
  - Create, update, delete, and query processes.
  - Process attributes include: name, status (running, suspended, blocked), priority (high, medium, low), detailed information, and logs.
- **Attribute Management**:
  - Modify the process's name, status, priority, detailed information, and logs.
  - Query historical logs of processes.
- **Query Functionality**:
  - Query processes based on priority and running status.

## Expected Technology Stack
- **Backend**: Use Python with the FastAPI framework.
- **Database**: Use SQLAlchemy to connect to SQLite.
- **Frontend**: Use HTML, CSS, and JavaScript.

## Referenced Open Source Projects
No specific open-source projects are referenced yet, but appropriate projects can be chosen for reference based on requirements.

# How to Quickly Deploy This Project

First, extract all the files of this project and note the path of the extracted folder.

Open the command prompt (cmd) and type the following command to check if Python is installed:
```cmd
python --version
```
If you don’t have a Python environment, follow the tutorial below to set it up:  
Refer to https://www.runoob.com/python3/python3-install.html

For example, my path is F:\ProcessManagement.  
So replace "folder_path" with F:\ProcessManagement in all commands.

In cmd, type:
```cmd
pip install -r folder_path\requirements.txt
```
To speed up installation, you can use:
```cmd
pip install -r folder_path\requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```
Wait for the installation to complete.

Then, create a `.ps1` script.  
First, create a new `.txt` file, copy the content below into it, and then rename the file extension to `.ps1`:
```
$url = "http://localhost:8000/"
Start-Process $url
cd folder_path
python main.py
```
Afterward, right-click the `.ps1` file and select "Run with PowerShell" from the context menu.

If it shows that execution is not allowed or the window closes immediately after opening, run the following command in PowerShell as an administrator:
```
Set-ExecutionPolicy RemoteSigned
```
Then type `Y` to confirm.