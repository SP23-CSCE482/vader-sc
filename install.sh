#!/bin/bash

PYTHON_VERSION=`python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))'`

# Check if Python version is at least 3.8
if (( $(echo "$PYTHON_VERSION < 3.6" | bc -l) )); then
    echo "ERROR: Python version must be at least 3.8"
    exit 1
else
    echo "Python version is at least 3.8. Continuing installation..."
fi

# Function to install exuberant-ctags from source
install_ctags() {
    echo "Installing exuberant-ctags from source..."
    # Download and extract source code
    wget "http://downloads.sourceforge.net/project/ctags/ctags/5.8/ctags-5.8.tar.gz"
    tar -xvzf ctags-5.8.tar.gz
    cd ctags-5.8
    # Configure, make, and install
    ./configure && make && make install
    # Clean up
    cd ..
    rm -rf ctags-5.8*
    echo "Installation of exuberant-ctags complete."
}

# Check if user has venv installed and in PATH
apt-get update
apt-get install python3-venv -y

# Check if exuberant-ctags is already installed
if ! type "ctags" > /dev/null; then
    # Check if user is root
    if [[ $EUID -ne 0 ]]; then
        echo "Exuberant-ctags is not installed. Building from source..."
        install_ctags
    else
        echo "Exuberant-ctags is not installed. Installing using apt-get..."
        apt-get install exuberant-ctags
    fi
else
    echo "Exuberant-ctags is already installed. Skipping installation..."
fi

# Upgrade pip and install requirements
python3 -m venv SC_Venv
SC_Venv/bin/python3 -m pip install --upgrade pip
SC_Venv/bin/python3 -m pip install -r requirements.txt -vvv

# Download custom CodeT5 model
echo "Do you want to download our custom CodeT5 model? (y/n)"
read response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]
then
    wget https://storage.googleapis.com/model_bucket_for_capstone_tamu/pytorch_model.bin 
fi

# Add alias to .bashrc file
echo "The 'vader-sc' alias has not been added to your .bashrc file. You can add it manually by running 'echo \"alias vader-sc='$PWD/SC_Venv/bin/python3 $PWD/vader.py'\" >> ~/.bashrc' to access from anywhere."
echo "To use Vader without alias, you must first activate the virtual environment by running 'source SC_Venv/bin/activate' and then run 'python3 vader.py'."


echo "Installation complete."
