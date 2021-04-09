FROM gitpod/workspace-full-vnc:latest

USER gitpod

RUN sudo apt-get update && sudo apt-get install -y \
    python3-tk tk8.6-dev python-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev libsdl1.2-dev libsmpeg-dev python-numpy subversion libportmidi-dev ffmpeg libswscale-dev libavformat-dev libavcodec-dev
    
#RUN pip3 install pytest==4.4.2 mock pytest-testdox toml && npm i breathecode-cli@1.2.59 -g
