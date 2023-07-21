# set base image (host OS)


#RUN adduser -S mosquitto
#
#RUN apk add --no-cache mosquitto-clients~1.5 mosquitto~1.5 su-exec
#
#EXPOSE 1883 9001

#RUN service mosquitto restart
#FROM alpine:edge
#RUN apk update && apk upgrade && apk add python3 && apk add py3-pip && apk add vim

#RUN python3 -m pip install --upgrade pip

FROM python:3.8

RUN apt update && apt upgrade && apt install nano && apt install iptables &

# set the working directory in the container
WORKDIR /code

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY . .

# command to run on container start
CMD [ "python", "-u", "./data_producer.py" ]