FROM python:2.7

MAINTAINER andyccs

ADD ./ /main

WORKDIR /main
RUN pip install -r ./requirements.txt

WORKDIR /main/src

EXPOSE 80

CMD ["python", "./manage.py", "runserver", "0.0.0.0:80"]
