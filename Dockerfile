# use the python image, alpine version
FROM python:3.9-alpine3.13
# specifiy the maintainer
LABEL maintainer="sivamjith@gmail.com"

# tells python that the output should be printed directly to the console
ENV PYTHONUNBUFFERED 1 

#copy the requirements.txt to the docker image
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt

# copy the Django app to the app folder in the image
COPY ./app /app

# set the working directory. when the commands are run, it will be automatically run from this directory
WORKDIR /app

EXPOSE 8000

# runs the command on the docker image
# every line creates a image snapshot on top of the previous command. So we need to minimise the number of commands as much as possible
# \ helps to breakdown the commands into new lines
# ideally there should be no virtual environment needed for python when we use docker. 
# we are adding a venv just to cater to some edge cases

ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
    then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    # add a new user in the image. the best practice is not to use the root user in the image, for security reasons
    adduser \
    --disabled-password \
    --no-create-home \
    django-user

# updates the environment variable PATH
ENV PATH="/py/bin:$PATH"

#this should be the last line of the dockerfile
USER django-user