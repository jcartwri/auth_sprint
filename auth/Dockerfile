FROM python:3.9

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ADD ./requirements.txt /usr/src/app

RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r /usr/src/app/requirements.txt

#COPY .. .
COPY . .
#
#COPY ./tests tests
CMD ["sh", "-c", "flask db upgrade ; python3 pywsgi.py"]
