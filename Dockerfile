FROM python:3.9.2

WORKDIR /app
COPY main.py main.py

RUN python3 -m pip install plexapi python-telegram-bot

ENV PYTHONUNBUFFERED=1
CMD ["python", "main.py"]