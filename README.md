# Rebels Render Repository

Welcome to the Rebels Render Repository! This README is designed to guide both technical and non-technical individuals through the steps necessary to use our software. We aim to make the process as smooth and straightforward as possible. Let's get started!

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Setup](#setup)
3. [Rendering the Collection](#rendering-the-collection)

## Prerequisites

Before starting the setup, ensure you have the required tools and dependencies based on your operating system:

### All Platforms:

1. **Git:** To clone the repository.

### Windows:

Please note, the provided instructions primarily cater to MacOS and Linux users. For Windows users, it is recommended to use [WSL (Windows Subsystem for Linux)](https://docs.microsoft.com/en-us/windows/wsl/install) to follow the Linux instructions.

### MacOS:

1. **Homebrew:** A package manager for MacOS.

Follow the instructions on the [Official Homebrew Website](https://docs.brew.sh/Installation):

```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

2. **Coreutils:** For the "timeout" command.
```
brew install coreutils
```

### Linux:

Ensure your package manager is updated.

## Setup

1. **Clone the repository:** Clone the repository by running the following command in your terminal:
```
git clone https://github.com/rebelsbynight/rebels-render
```

2. **Change directory:** Navigate into the cloned repository:
```
cd rebels-render
```

3. **Install Python3:** Ensure Python3 is installed on your system.
- MacOS: 
```
brew install python3
```
- Linux (Debian-based systems): 
```
sudo apt-get update
sudo apt-get install python3
```

4. **Install Blender 3.1.2:** Make sure to have Blender 3.1.2 installed.
- Download the appropriate version for your system from the [Blender website](https://www.blender.org/download/).

5. **Download and Unzip the 3D Files:**
- Download the Rebels 3D files' zip from the provided URL and name the folder Rebels-3D-Files
```

```
- Unzip the downloaded archive in the current directory. You can use the default tools in MacOS and Linux, or tools like WinZip or 7-Zip on Windows.

## Rendering the Collection

Based on your operating system, follow the below instructions:

### MacOS:

Run the following commands in the terminal:
```
while true ; do
    timeout 1800 /Applications/Blender.app/Contents/MacOS/Blender -b ./Rebels-3D-Files/3D-Files/render_file_optimized.blend --engine BLENDER_EEVEE -o . -P ./gen-collection-optimized.py -- ./new_collection_map.json
    sleep 15 # A short sleep to ensure that the process has fully terminated before re-running
done
```

### Linux:

Run the following commands in the terminal:
```
while true ; do
    timeout 1800 blender -b ./Rebels-3D-Files/render_file_optimized.blend --engine BLENDER_EEVEE -o . -P ./gen-collection-optimized.py -- ./new_collection_map.json
    sleep 15 # A short sleep to ensure that the process has fully terminated before re-running
done
```

## License
The code and 3D files can used in any way you'd like so long as it's applied for the Rebels project and Rebels NFTs, any other use is prohibited.

Thank you for using the Rebels rendering infrastructure!
