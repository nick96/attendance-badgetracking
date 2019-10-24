FROM python:3.7

WORKDIR /api

RUN apt-get update && apt-get install -y postgresql

COPY requirements.txt requirements.txt
COPY vendor vendor
RUN pip install -r requirements.txt

COPY migrations migrations
COPY ./scripts/*.sh ./scripts/
COPY *.py ./

COPY ./scripts/boot.sh ./scripts/boot.sh
COPY scripts/wait-for-postgres.sh ./scripts/wait-for-postgres.sh
RUN chmod +x ./scripts/boot.sh
RUN chmod +x ./scripts/wait-for-postgres.sh

CMD ["./scripts/wait-for-postgres.sh", "postgres:5432", "--", "./scripts/boot.sh"]