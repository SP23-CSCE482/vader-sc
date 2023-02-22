# Vader-SC

This is the repository for VADER-SC - A project to increase source code readability.

## Usage

To parse directory run `SC_Venv/bin/python3.10 vader.py /path/to/directory`

## Local Setup

Install Docker

-Build the Docker image
-Run `docker build -t vader-sc -f Dockerfile .`

-Once the image is built, run the image
-Run `docker run -it vader-sc /bin/bash`
