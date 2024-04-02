FROM jenkins/jenkins:latest
USER root
RUN mkdir /my_app
WORKDIR /my_app
RUN pwd
RUN ls -la
RUN apt-get update
RUN apt-get install -y python3-pip