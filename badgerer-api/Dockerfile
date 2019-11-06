FROM python:3.7.4 as linter

WORKDIR /badgerer-api

RUN python3 -m pip install poetry
COPY ./pyproject.toml ./pyproject.toml
COPY ./poetry.lock ./poetry.lock
RUN poetry install

COPY ./mypy.ini ./mypy.ini

COPY ./e2e_tests/*.py ./e2e_tests/
COPY ./tests/*.py ./tests/
COPY ./badgerer_api/*.py ./badgerer_api/

CMD ["bash", "-c", "poetry run mypy ./badgerer_api && flake8"]

FROM python:3.7.4 as unit_testing

WORKDIR /badgerer-api

RUN python3 -m pip install poetry
COPY ./pyproject.toml ./pyproject.toml
COPY ./poetry.lock ./poetry.lock
RUN poetry install

COPY --from=linter /badgerer-api/badgerer_api /badgerer-api/badgerer_api
COPY --from=linter /badgerer-api/tests /badgerer-api/tests

CMD ["poetry", "run", "pytest", "tests", "--cov", "badgerer_api"]


FROM python:3.7.4 as integration_testing

WORKDIR /badgerer-api

RUN apt-get update && apt-get install -y postgresql
RUN python3 -m pip install poetry
COPY --from=unit_testing /badgerer-api/pyproject.toml ./pyproject.toml
COPY --from=unit_testing /badgerer-api/poetry.lock ./poetry.lock
RUN poetry install

COPY ./scripts/boot.sh ./scripts/boot.sh
COPY ./scripts/wait-for-postgres.sh ./scripts/wait-for-postgres.sh

RUN chmod +x ./scripts/boot.sh
RUN chmod +x ./scripts/wait-for-postgres.sh

COPY migrations migrations
COPY --from=linter /badgerer-api/e2e_tests/*.py ./e2e_tests/
COPY --from=unit_testing /badgerer-api/badgerer_api ./badgerer_api

CMD ["poetry", "run", "pytest", "./e2e_tests"]

FROM python:3.7.4 as builder

WORKDIR /badgerer-api

RUN python3 -m pip install poetry
COPY --from=unit_testing /badgerer-api/pyproject.toml ./pyproject.toml
COPY --from=unit_testing /badgerer-api/poetry.lock ./poetry.lock
RUN poetry install --no-dev

COPY --from=unit_testing /badgerer-api/badgerer_api ./badgerer_api
RUN poetry build --format wheel

FROM python:3.7.4

WORKDIR /dist

RUN apt-get update && apt-get install -y postgresql
COPY --from=builder /badgerer-api/dist/*.whl ./
RUN python3 -m pip install *.whl

CMD ["./scripts/wait-for-postgres.sh", "postgres:5432", "--", "poetry run ./scripts/boot.sh badgerer_api"]
