FROM python:3.10

COPY ./requirements.txt app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 3000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000", "--reload"]