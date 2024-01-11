FROM python:3.10-alpine

WORKDIR .
COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

ENV FLASK_APP app.py
ENV FLASK_ENV development
ENV FLASK_RUN_PORT 5000
ENV FLASK_RUN_HOST 0.0.0.0

EXPOSE 5000

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
