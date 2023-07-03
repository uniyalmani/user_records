FROM python:3.9

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR /usr/src/app

ENV FLASK_APP=app.py

CMD ["flask", "run", "--host=0.0.0.0"]