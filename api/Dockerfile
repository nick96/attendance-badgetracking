FROM python:3.7 as linter

WORKDIR /api

RUN python3 -m pip install mypy flake8
COPY ./e2e_tests ./e2e_tests
COPY ./api ./api

CMD ["mypy", "./api", "&&", "flake8"]

FROM python:3.7 as unit_testing

WORKDIR /api

COPY --from=linter /api /api

COPY ./requirements.txt ./requirements.txt

RUN python3 -m pip install -r requirements.txt

CMD ["pytest", "./api/tests"]


FROM python:3.7 as integration_testing

RUN apt-get update && apt-get install -y postgresql
COPY ./scripts/boot.sh ./scripts/boot.sh
COPY ./scripts/wait-for-postgres.sh ./scripts/wait-for-postgres.sh

RUN chmod +x ./scripts/boot.sh
RUN chmod +x ./scripts/wait-for-postgres.sh

COPY migrations migrations

COPY --from=testing /api /api

RUN python -m pip install -r requirements.txt

CMD ["pytest", "./e2e_tests"]

FROM python:3.7

RUN apt-get update && apt-get install -y postgresql
COPY ./scripts/boot.sh ./scripts/boot.sh
COPY ./scripts/wait-for-postgres.sh ./scripts/wait-for-postgres.sh

RUN chmod +x ./scripts/boot.sh
RUN chmod +x ./scripts/wait-for-postgres.sh

COPY migrations migrations

COPY --from=testing /api /api

RUN python -m pip install -r requirements.txt

CMD ["./scripts/wait-for-postgres.sh", "postgres:5432", "--", "./scripts/boot.sh"]
