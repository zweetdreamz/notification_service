FROM python:3.10

RUN mkdir /notif_app

WORKDIR /notif_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

WORKDIR app

CMD uvicorn main:app --port 8000 --host 0.0.0.0