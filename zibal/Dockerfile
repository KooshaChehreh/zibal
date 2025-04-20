FROM docker.arvancloud.ir/python:3.12

WORKDIR ./app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "--reload", "--workers=4", "--worker-tmp-dir", "/dev/shm", "--bind=0.0.0.0:8000", "--chdir", "/app/zibal", "zibal.wsgi"]

