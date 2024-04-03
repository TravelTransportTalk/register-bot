FROM docker.io/library/python:3.12-alpine

RUN adduser -DH runner
WORKDIR /app
ENV PATH /env/bin:$PATH

ENTRYPOINT ["python", "/app/bot.py"]

ADD --chown=runner ./requirements.txt /app/requirements.txt
RUN python -m venv /env && pip install -r requirements.txt

ADD --chown=runner bot.py /app/
ADD --chown=runner src /app/src
