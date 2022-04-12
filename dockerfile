# syntax=docker/dockerfile:1

FROM ubuntu:latest
WORKDIR /app

RUN apt-get update && apt-get autoclean

RUN apt-get update && apt-get install -y --no-install-recommends python3-pip

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

RUN pip3 install pyqt5

RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN apt-get install libgtk2.0-dev -y

RUN apt-get install -y '^libxcb.*-dev' libx11-xcb-dev libglu1-mesa-dev libxrender-dev libxi-dev libxkbcommon-dev libxkbcommon-x11-dev 

ENV QT_X11_NO_MITSHM=1

# RUN export DISPLAY=:0.0

COPY . .

#CMD [ "python3", "-m", "src", "hootl.yaml", "NoSIM"]

#CMD [ "python3", "-m", "src"]