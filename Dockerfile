FROM python:3.8-alpine

EXPOSE 8080

RUN mkdir /app
WORKDIR /app
COPY . /app/

RUN pip install -r requirements.txt

CMD [ "python", "src/app.py" ]