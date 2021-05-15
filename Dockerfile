FROM python:3.9.4-slim-buster

WORKDIR /stockbird

RUN apt-get update

RUN apt-get -y install stockfish

ENV PATH="/usr/games:${PATH}"

RUN pip install --upgrade pip

COPY . .

RUN pip install -r requirements.txt

RUN chmod +x main.py

CMD ./main.py
