import os
import random
import shutil
import subprocess
import requests
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading

# Define server list storage path
SERVER_LIST_PATH = os.path.join(os.getenv('USERPROFILE'), 'AppData', 'Local', 'PaperMCDownloader')
os.makedirs(SERVER_LIST_PATH, exist_ok=True)
SERVER_LIST_FILE = os.path.join(SERVER_LIST_PATH, 'servers.txt')

# Global list to store server information
servers = []

# Versions dictionary
VERSIONS = {
    "1.21.4": "https://api.papermc.io/v2/projects/paper/versions/1.21.4/builds/173/downloads/paper-1.21.4-173.jar",
    "1.21.3": "https://api.papermc.io/v2/projects/paper/versions/1.21.3/builds/82/downloads/paper-1.21.3-82.jar",
    "1.21.1": "https://api.papermc.io/v2/projects/paper/versions/1.21.1/builds/132/downloads/paper-1.21.1-132.jar",
    "1.21": "https://api.papermc.io/v2/projects/paper/versions/1.21/builds/130/downloads/paper-1.21-130.jar",
    "1.20.6": "https://api.papermc.io/v2/projects/paper/versions/1.20.6/builds/151/downloads/paper-1.20.6-151.jar",
    "1.20.5": "https://api.papermc.io/v2/projects/paper/versions/1.20.5/builds/22/downloads/paper-1.20.5-22.jar",
    "1.20.4": "https://api.papermc.io/v2/projects/paper/versions/1.20.4/builds/499/downloads/paper-1.20.4-499.jar",
    "1.20.2": "https://api.papermc.io/v2/projects/paper/versions/1.20.2/builds/318/downloads/paper-1.20.2-318.jar",
    "1.20.1": "https://api.papermc.io/v2/projects/paper/versions/1.20.1/builds/196/downloads/paper-1.20.1-196.jar",
    "1.20": "https://api.papermc.io/v2/projects/paper/versions/1.20/builds/17/downloads/paper-1.20-17.jar",
    "1.19.4": "https://api.papermc.io/v2/projects/paper/versions/1.19.4/builds/550/downloads/paper-1.19.4-550.jar",
    "1.19.3": "https://api.papermc.io/v2/projects/paper/versions/1.19.3/builds/448/downloads/paper-1.19.3-448.jar",
    "1.19.2": "https://api.papermc.io/v2/projects/paper/versions/1.19.2/builds/307/downloads/paper-1.19.2-307.jar",
    "1.19.1": "https://api.papermc.io/v2/projects/paper/versions/1.19.1/builds/111/downloads/paper-1.19.1-111.jar",
    "1.19": "https://api.papermc.io/v2/projects/paper/versions/1.19/builds/81/downloads/paper-1.19-81.jar",
    "1.18.2": "https://api.papermc.io/v2/projects/paper/versions/1.18.2/builds/388/downloads/paper-1.18.2-388.jar",
    "1.18.1": "https://api.papermc.io/v2/projects/paper/versions/1.18.1/builds/216/downloads/paper-1.18.1-216.jar",
    "1.18 (Experimental)": "https://api.papermc.io/v2/projects/paper/versions/1.18/builds/66/downloads/paper-1.18-66.jar",
    "1.17.1": "https://api.papermc.io/v2/projects/paper/versions/1.17.1/builds/318/downloads/paper-1.17.1-318.jar",
    "1.17": "https://api.papermc.io/v2/projects/paper/versions/1.17/builds/79/downloads/paper-1.17-79.jar",
    "1.16.5": "https://api.papermc.io/v2/projects/paper/versions/1.16.5/builds/794/downloads/paper-1.16.5-794.jar",
    "1.16.4": "https://api.papermc.io/v2/projects/paper/versions/1.16.4/builds/416/downloads/paper-1.16.4-416.jar",
    "1.16.3": "https://api.papermc.io/v2/projects/paper/versions/1.16.3/builds/253/downloads/paper-1.16.3-253.jar",
    "1.16.2": "https://api.papermc.io/v2/projects/paper/versions/1.16.2/builds/189/downloads/paper-1.16.2-189.jar",
    "1.16.1": "https://api.papermc.io/v2/projects/paper/versions/1.16.1/builds/138/downloads/paper-1.16.1-138.jar",
    "1.15.2": "https://api.papermc.io/v2/projects/paper/versions/1.15.2/builds/393/downloads/paper-1.15.2-393.jar",
    "1.15.1": "https://api.papermc.io/v2/projects/paper/versions/1.15.1/builds/62/downloads/paper-1.15.1-62.jar",
    "1.15": "https://api.papermc.io/v2/projects/paper/versions/1.15/builds/21/downloads/paper-1.15-21.jar",
    "1.14.4": "https://api.papermc.io/v2/projects/paper/versions/1.14.4/builds/245/downloads/paper-1.14.4-245.jar",
    "1.14.3": "https://api.papermc.io/v2/projects/paper/versions/1.14.3/builds/134/downloads/paper-1.14.3-134.jar",
    "1.14.2": "https://api.papermc.io/v2/projects/paper/versions/1.14.2/builds/107/downloads/paper-1.14.2-107.jar",
    "1.14.1": "https://api.papermc.io/v2/projects/paper/versions/1.14.1/builds/50/downloads/paper-1.14.1-50.jar",
    "1.14": "https://api.papermc.io/v2/projects/paper/versions/1.14/builds/17/downloads/paper-1.14-17.jar",
    "1.13.2": "https://api.papermc.io/v2/projects/paper/versions/1.13.2/builds/657/downloads/paper-1.13.2-657.jar",
    "1.13.1": "https://api.papermc.io/v2/projects/paper/versions/1.13.1/builds/386/downloads/paper-1.13.1-386.jar",
    "1.13": "https://api.papermc.io/v2/projects/paper/versions/1.13/builds/173/downloads/paper-1.13-173.jar",
    "1.13-pre7 (Prerelease)": "https://api.papermc.io/v2/projects/paper/versions/1.13-pre7/builds/12/downloads/paper-1.13-pre7-12.jar",
    "1.12.2": "https://api.papermc.io/v2/projects/paper/versions/1.12.2/builds/1620/downloads/paper-1.12.2-1620.jar",
    "1.12.1": "https://api.papermc.io/v2/projects/paper/versions/1.12.1/builds/1204/downloads/paper-1.12.1-1204.jar",
    "1.12": "https://api.papermc.io/v2/projects/paper/versions/1.12/builds/1169/downloads/paper-1.12-1169.jar",
    "1.11.2": "https://api.papermc.io/v2/projects/paper/versions/1.11.2/builds/1106/downloads/paper-1.11.2-1106.jar",
    "1.10.2": "https://api.papermc.io/v2/projects/paper/versions/1.10.2/builds/918/downloads/paper-1.10.2-918.jar",
    "1.9.4": "https://api.papermc.io/v2/projects/paper/versions/1.9.4/builds/775/downloads/paper-1.9.4-775.jar",
    "1.8.8/1.8.9": "https://api.papermc.io/v2/projects/paper/versions/1.8.8/builds/445/downloads/paper-1.8.8-445.jar"
}

class MinecraftServer:
    def __init__(self, name, directory, version, port=None):
        self.name = name
        self.directory = directory
        self.version = version
        self.port = port if port else random.randint(25000, 35000)  # Random port
        self.process = None

    def setup_server(self):
        os.makedirs(self.directory, exist_ok=True)
        jar_url = VERSIONS.get(self.version)
        jar_path = os.path.join(self.directory, "server.jar")
        
        # Show loading message
        loading_label.config(text=f"Setting up {self.name}...")
        root.update()
        
        # Download PaperMC jar
        response = requests.get(jar_url, stream=True)
        if response.status_code == 200:
            with open(jar_path, 'wb') as file:
                shutil.copyfileobj(response.raw, file)
        else:
            messagebox.showerror("Download Error", "Failed to download PaperMC server.")
            return

        # Run server once to generate files
        subprocess.run(["java", "-jar", jar_path], cwd=self.directory)

        # Accept EULA
        eula_path = os.path.join(self.directory, "eula.txt")
        if os.path.exists(eula_path):
            with open(eula_path, 'r') as file:
                eula_content = file.read().replace("eula=false", "eula=true")
            with open(eula_path, 'w') as file:
                file.write(eula_content)

        # Configure server.properties
        properties_path = os.path.join(self.directory, "server.properties")
        properties_content = f"""
#Minecraft server properties
server-port={self.port}
query.port={self.port}
rcon.port={self.port+1}
motd=A Minecraft Server
online-mode=true
gamemode=survival
max-players=20
        """.strip()
        
        with open(properties_path, 'w') as file:
            file.write(properties_content)
        
        # Remove loading message
        loading_label.config(text="")
        save_servers()

    def start_server(self):
        if self.process is None:
            self.process = subprocess.Popen(["java", "-jar", "server.jar"], cwd=self.directory, stdin=subprocess.PIPE)

    def stop_server(self):
        if self.process:
            self.process.stdin.write(b"stop\n")
            self.process.stdin.flush()
            self.process.wait()
            self.process = None

    def restart_server(self):
        self.stop_server()
        self.start_server()

    def delete_server(self):
        servers.remove(self)
        save_servers()
        update_server_list()
        messagebox.showinfo("Server Deleted", f"Server {self.name} deleted.")

# Save servers to file
def save_servers():
    with open(SERVER_LIST_FILE, 'w') as file:
        for server in servers:
            file.write(f"{server.name},{server.directory},{server.version},{server.port}\n")

# Load servers from file
def load_servers():
    if os.path.exists(SERVER_LIST_FILE):
        with open(SERVER_LIST_FILE, 'r') as file:
            for line in file:
                name, directory, version, port = line.strip().split(',')
                servers.append(MinecraftServer(name, directory, version, int(port)))

# GUI Functions
def create_server():
    directory = filedialog.askdirectory()
    if not directory:
        return
    name = tk.simpledialog.askstring("Server Name", "Enter server name:")
    if not name:
        return
    
    # Create version selection window
    version_window = tk.Toplevel(root)
    version_window.title("Select Minecraft Version")
    version_window.geometry("300x150")
    
    tk.Label(version_window, text="Select version:").pack(pady=5)
    version_var = tk.StringVar()
    version_dropdown = ttk.Combobox(version_window, textvariable=version_var, values=list(VERSIONS.keys()), state="readonly")
    version_dropdown.pack(pady=5)
    version_dropdown.current(0)
    
    def confirm_version():
        version_window.destroy()
        version = version_var.get()
        if version not in VERSIONS:
            messagebox.showerror("Invalid Version", "Selected version is not available.")
            return

        server = MinecraftServer(name, directory, version)
        thread = threading.Thread(target=server.setup_server)
        thread.start()
        servers.append(server)
        update_server_list()
        save_servers()
    
    tk.Button(version_window, text="Confirm", command=confirm_version).pack(pady=10)
    

def update_server_list():
    for widget in frame_servers.winfo_children():
        widget.destroy()
    for server in servers:
        row = tk.Frame(frame_servers)
        row.pack(fill='x', padx=5, pady=5)
        tk.Label(row, text=f"{server.name} (Port: {server.port}, Version: {server.version})", font=("Arial", 12)).pack(side='left', padx=5)
        tk.Button(row, text='Start', command=server.start_server).pack(side='left', padx=2)
        tk.Button(row, text='Stop', command=server.stop_server).pack(side='left', padx=2)
        tk.Button(row, text='Restart', command=server.restart_server).pack(side='left', padx=2)
        tk.Button(row, text='Delete', command=lambda s=server: s.delete_server()).pack(side='left', padx=2)

# Tkinter UI
root = tk.Tk()
root.title("Minecraft PaperMC Server Manager")
root.geometry("500x400")

btn_create = tk.Button(root, text="Create Server", font=("Arial", 14), command=create_server)
btn_create.pack(pady=10)

loading_label = tk.Label(root, text="", font=("Arial", 12), fg="red")
loading_label.pack()

frame_servers = tk.Frame(root)
frame_servers.pack(fill='both', expand=True, padx=10, pady=10)

load_servers()
update_server_list()
root.mainloop()