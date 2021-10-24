FROM python:3.8-alpine

ENV APP_HOME /app
WORKDIR $APP_HOME

ADD . /app

RUN pip install -r requirements.txt

CMD [ "python", "src/app.py" ]