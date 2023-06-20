# pull official base image
FROM python:3.10

ENV APP_HOME=/usr/src/app
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/static
RUN mkdir $APP_HOME/media
WORKDIR $APP_HOME
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apt-get update  \
    && apt-get install netcat-traditional -y  \
    && apt-get install -y postgresql-server-dev-all gcc python3-dev musl-dev

# install dependencies
RUN pip install --upgrade pip

COPY ./requirements.txt .
RUN pip install -r requirements.txt


COPY ./entrypoint.sh .

RUN ["chmod", "+x", "/usr/src/app/entrypoint.sh"]

# copy project
COPY . .

RUN sed -i 's/\r$//g'  $APP_HOME/entrypoint.sh
RUN chmod +x  $APP_HOME/entrypoint.sh

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]