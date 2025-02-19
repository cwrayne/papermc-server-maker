# PaperMC Server Maker
 
A python app to easily make a Minecraft PaperMC server. 

## Installing

### Installer
From the releases, download the latest windows zip. Extract the zip and run the exe as administrator. Wait for it to finish, and then launch it by searching "PaperMC Server Maker" in the search bar of Windows.

### Portable version
From the releases, download the latest portable windows zip. Extract the zip and run the exe as administrator, and you will launch the app

## Usage

Once you have got into the app, click "Create" to make a server. Choose a directory, choose your version and server name, and then wait for it to create. Then there will be a server port; this is what you will connect to in Minecraft. press "start" to start the server, and then launch Minecraft and connect to localhost:port where port is your server port. the other buttons explain themselves

## Building

1. Clone the repo
2. Install pyinstaller using pip
3. `python -m pyinstaller app.py` *(For installer, use `python -m pyinstaller ./installer/install.py)*
4. Open dist/app.exe *(For installer, installer/dist/install.exe)*
