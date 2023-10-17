FROM python:3.8-slim-bullseye

COPY requirements.txt .
RUN pip3 install --upgrade pip setuptools wheel
RUN pip3 install -r requirements.txt
COPY . .
CMD python3 -u app.py