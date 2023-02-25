FROM python:3.10-slim as base

WORKDIR /heb_interview/

# https://python-poetry.org/docs#ci-recommendations
ENV POETRY_VERSION=1.3.2
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv

# Tell Poetry where to place its cache and virtual environment
ENV POETRY_CACHE_DIR=/opt/.cache

RUN apt-get update && apt-get -y install libpq-dev gcc

FROM base as poetry-base

# Creating a virtual environment just for poetry and install it with pip
RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}


FROM base as app-build

# Copy Poetry to app image
COPY --from=poetry-base ${POETRY_VENV} ${POETRY_VENV}

# Add `poetry` to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

COPY poetry.lock pyproject.toml ./

RUN poetry check


RUN poetry install --no-interaction --no-cache --without dev --no-root


COPY ./src .

CMD ["sh", "serve.sh"]

FROM app-build as prod
