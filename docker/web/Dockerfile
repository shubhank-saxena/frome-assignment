# pull official base image
FROM python:3.11

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# expose port
EXPOSE 8000

RUN apt-get update

# Upgrade pip and install pipenv
RUN pip install --upgrade pip
RUN pip install pipenv

# copy Pipfile
COPY ./Pipfile ./Pipfile.lock /usr/src/app/

# install dependencies
RUN pipenv install --system --deploy --ignore-pipfile

# copy project
COPY . /usr/src/app/

CMD [ "python", "manage.py", "collectstatic" ]
