#FROM python:3.12.10-alpine3.21
#FROM ubuntu:latest
FROM python:3.13
WORKDIR /code

COPY notifier/ /code/notifier
COPY --chmod=0755 config/install_sdtrunk_jmbe_creator.sh /code

RUN apt update 
RUN DEBIAN_FRONTEND=noninteractive TZ="America/New_York" apt install -y python3-pip 
RUN pip3 install pipenv
RUN cd /code/notifier && pipenv install --system --deploy 
RUN /code/install_sdtrunk_jmbe_creator.sh
RUN mkdir /root/SDRTrunk; mkdir /root/SDRTrunk/playlist/
RUN python /code/notifier/create_playlist.py > /root/SDRTrunk/playlist/default.xml
RUN python /code/notifier/create_scripts.py
CMD ["/code/sdr-trunk-linux-x86_64-v0.6.1/bin/sdr-trunk"]

