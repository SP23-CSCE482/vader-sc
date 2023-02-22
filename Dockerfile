FROM ubuntu:jammy
SHELL ["/bin/bash", "-c"]

RUN apt-get update -y \
    && apt-get upgrade -y

WORKDIR ./vader-sc
#copy neccessary files into docker container
COPY FunctionExtract/ FunctionExtract/
COPY Sample_Code/ Sample_Code/
COPY vader.py vader.py
COPY requirements.txt requirements.txt

#install python and pip
RUN apt-get install -y Python3.10
RUN apt-get install python3-pip -y
RUN apt-get install python3.10-venv -y

#create python venv and install requirements
RUN python3.10 -m venv SC_Venv
RUN apt-get install exuberant-ctags -y
RUN source SC_Venv/bin/activate && pip install -r requirements.txt vvv