FROM python:3-slim

WORKDIR /usr/src/app

COPY ./requirements.txt ./

RUN pip install -r ./requirements.txt

COPY . .

EXPOSE 8201

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8201", "--log-level", "debug"]