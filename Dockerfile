FROM python:latest

WORKDIR /app

COPY . /app/

RUN apt-get update && apt-get install -y make

RUN apt install make

RUN pip install -r requirements.txt

RUN chmod +x ./entrypoint.sh

EXPOSE 8000

ENTRYPOINT [ "./entrypoint.sh" ]