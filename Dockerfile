# start by pulling the python image
FROM python:3.8.6-slim

# copy the requirements file into the image
COPY ./requirements.txt /requirements.txt

# install the dependencies and packages in the requirements file
RUN python3 -m pip install -r requirements.txt
RUN rm /requirements.txt

# install ffmpeg tool
RUN apt update -y && apt upgrade -y
RUN apt -y install ffmpeg

# copy every content from the local file to the image
COPY ./app /app
WORKDIR /app

# Expose port outside docker container
EXPOSE 9999

# configure the container to run in an executed manner
ENTRYPOINT [ "python", "server.py" ]