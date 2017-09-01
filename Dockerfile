FROM python:2.7

MAINTAINER andyccs

ADD . /src

WORKDIR /src

RUN pip install -r ./requirements.txt

EXPOSE 80

CMD ["python", "./manage.py", "runserver", "0.0.0.0:80"]
