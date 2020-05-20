FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
ENV WEBHOOK_URL https://alertmanager.nglm.rt.ru:6443/api/v2/alerts
CMD ["gunicorn", "-w 3", "-b :8080", "-t 9000", "app:app"]
