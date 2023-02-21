FROM ubuntu:jammy
SHELL ["/bin/bash", "-c"]

RUN apt-get update -y \
    && apt-get upgrade -y

WORKDIR ./vader-sc
COPY * .

RUN apt-get install -y Python3.10
RUN apt-get install python3-pip -y
RUN apt-get install python3.10-venv -y

RUN python3.10 -m venv SC_Venv
RUN apt-get install exuberant-ctags -y
RUN source SC_Venv/bin/activate && pip install -r requirements.txt

#CMD ["./bin/bash"]