import os
import sys
import requests
import zipfile
import tempfile
import shutil

def download_file(url, local_filename):
    """
    Download a file from the given URL and save it locally.
    """
    response = requests.get(url, stream=True)
    response.raise_for_status()  # Raise an exception for HTTP errors
    with open(local_filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:  # Filter out keep-alive chunks
                f.write(chunk)
    return local_filename

def create_shortcut(target, shortcut_path, description=""):
    """
    Create a Windows shortcut (.lnk file) using the COM interface.
    """
    try:
        import win32com.client
    except ImportError:
        print("Error: pywin32 is required to create shortcuts. Install it via pip (pip install pywin32).")
        sys.exit(1)

    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.Targetpath = target
    shortcut.WorkingDirectory = os.path.dirname(target)
    shortcut.Description = description
    shortcut.save()

def main():
    # Ensure the script is running on Windows
    if os.name != 'nt':
        print("This script is designed to run on Windows.")
        sys.exit(1)

    # URL of the ZIP file to download
    url = "https://dashbenton.com/papermcdownloader/downloadthis.zip"

    # Define file and folder paths
    temp_dir = tempfile.gettempdir()
    zip_filename = os.path.join(temp_dir, "downloadthis.zip")
    target_directory = r"C:\Program Files\PaperMCServerMaker"
    app_exe = os.path.join(target_directory, "app.exe")
    shortcut_path = r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\PaperMC Server Maker.lnk"

    print("Downloading ZIP file...")
    try:
        download_file(url, zip_filename)
    except Exception as e:
        print(f"Failed to download file: {e}")
        sys.exit(1)

    print("Extracting ZIP file...")
    try:
        with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
            # Create the target directory if it doesn't exist
            os.makedirs(target_directory, exist_ok=True)
            zip_ref.extractall(target_directory)
    except Exception as e:
        print(f"Failed to extract ZIP file: {e}")
        sys.exit(1)

    print("Creating shortcut...")
    try:
        create_shortcut(app_exe, shortcut_path, "PaperMC Server Maker")
    except Exception as e:
        print(f"Failed to create shortcut: {e}")
        sys.exit(1)

    print("Installation complete.")

if __name__ == "__main__":
    main()
