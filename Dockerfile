FROM python:3.8-slim-buster

WORKDIR /app
COPY notion.py /app
COPY requirements.txt /app
COPY pretux_bot.py /app

RUN pip3 install -r requirements.txt

CMD ["python3", "pretux_bot.py"]