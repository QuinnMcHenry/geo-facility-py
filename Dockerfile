FROM python:3.9

WORKDIR /code

COPY app.py /code/app.py
COPY models.py /code/models.py
COPY routes.py /code/routes.py
COPY config.py /code/config.py 
COPY Chaminade-Seal.png /code/Chaminade-Seal.png
COPY /static /code/static
COPY /styles /code/styles

RUN chmod +rx /code/app.py