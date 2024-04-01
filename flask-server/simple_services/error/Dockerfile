FROM python:3-slim

WORKDIR /usr/src/app

COPY ./requirements.txt ./

RUN pip install -r ./requirements.txt

COPY ./app ./

CMD ["python", "main.py"]