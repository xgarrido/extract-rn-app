FROM ubuntu:22.04
MAINTAINER Xavier Garrido <xavier.garrido@lal.in2p3.fr>

RUN apt-get update && apt-get install -y \
        git                              \
        qpdf                             \
        python3                          \
        python3-pip

RUN python3 -m pip install --no-cache-dir notebook jupyterlab voila

# create user with a home directory
ARG NB_USER
ARG NB_UID
ENV USER ${NB_USER}
ENV HOME /home/${NB_USER}

RUN adduser --disabled-password \
    --gecos "Default user" \
    --uid ${NB_UID} \
    ${NB_USER}
WORKDIR ${HOME}
USER ${USER}

RUN git clone https://github.com/xgarrido/extract-rn-app.git
