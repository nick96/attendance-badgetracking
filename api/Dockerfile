FROM python:3.7

WORKDIR /api

RUN apt-get update && apt-get install -y postgresql

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY src/migrations migrations
COPY src/*.py ./

COPY ./scripts/boot.sh ./scripts/boot.sh
COPY scripts/wait-for-postgres.sh ./scripts/wait-for-postgres.sh
RUN chmod +x ./scripts/boot.sh
RUN chmod +x ./scripts/wait-for-postgres.sh

CMD ["./scripts/wait-for-postgres.sh", "postgres:5432", "--", "./scripts/boot.sh"]