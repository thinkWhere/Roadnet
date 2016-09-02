FROM ubuntu:14.04
MAINTAINER John A Stevenson <john.stevenson@thinkwhere.com>

# Set up repositories for latest QGIS

RUN sudo apt-get install -y software-properties-common
RUN sudo add-apt-repository -y ppa:ubuntugis/ubuntugis-unstable
RUN sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-key 3FF5FFCAD71472C4
RUN sudo touch /etc/apt/sources.list.d/qgis-ubuntugis.list
RUN echo "deb http://qgis.org/ubuntugis trusty main" | \
        sudo tee -a  /etc/apt/sources.list.d/qgis-ubuntugis.list

RUN sudo apt-get update
RUN sudo apt-get install -y \
    build-essential \
    git \
    python-dev \
    python-pip \
    python-pyspatialite \
    python-qt4-sql \
    qgis \
    qt4-designer \
    qt4-dev-tools \
    unixodbc-dev \
    xvfb

RUN sudo pip install \
    boto3 \
    coverage \
    mock \
    nose \
    pyodbc

# Xvfb is a fake X server
ENV DISPLAY=:1
RUN sudo Xvfb :1 &

