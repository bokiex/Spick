FROM python:3-slim

WORKDIR /usr/src/app

ENV DATABASE_URL=mysql+mysqlconnector://root:root@localhost:8889/reservation

COPY ./requirements.txt ./

RUN pip install -r ./requirements.txt

COPY ./app ./

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8102"]