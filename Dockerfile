FROM python:3.10-alpine
LABEL org-opencontainer.image.authors="jan@macenka.de"
LABEL maintainer="FritzBoxRestarter@macenka.de"
WORKDIR /code
COPY ./requirements.txt .
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]