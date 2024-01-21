FROM python:3.10-alpine

# where to put in linux env
WORKDIR /app
COPY requirements.txt .
COPY app.py .
COPY .env .
COPY migrations .
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add --no-cache mariadb-dev

RUN pip install -r requirements.txt


RUN apk del build-deps

ENV FLASK_APP app.py
ENV FLASK_ENV development
# default port is 5000, but changing to 8000
ENV FLASK_RUN_PORT 8000
ENV FLASK_RUN_HOST 0.0.0.0

EXPOSE 8000

CMD ["flask", "run"]

#FROM builder AS dev-envs

#RUN <<EOF
#apk update
#apk add git
#EOF

#RUN <<EOF
#addgroup -S docker
#adduser -S --shell /bin/bash --ingroup docker vscode
#EOF

# install Docker tools (cli, buildx, compose)
#COPY --from=gloursdocker/docker / /

#CMD ["flask", "run"]
