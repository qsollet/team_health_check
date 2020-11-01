FROM python:3.8-slim

LABEL maintainer=quentin@sollet.fr

RUN useradd --create-home --shell /bin/bash appuser
USER appuser
ENV PATH="/home/appuser/.local/bin:${PATH}"

ENV GUNICORN_BIND_IP 0.0.0.0
ENV GUNICORN_BIND_PORT 8080
# Can use only one worker as using a global variable
ENV GUNICORN_WORKER 1

COPY . /home/appuser/src
WORKDIR /home/appuser/src
RUN pip install --user gunicorn && pip install --user -r requirements.txt

ENTRYPOINT ["./run.sh"]
