FROM python:3.10-alpine

WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN pip install pipenv \
 && pipenv install --deploy --system \
 && pip uninstall pipenv -y

COPY . .

CMD ["python", "-m", "tado_autoassist"]
