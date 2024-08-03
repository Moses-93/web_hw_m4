FROM python:3.12.4-slim

WORKDIR /web_hw_m4

COPY . /web_hw_m4

CMD [ "python", "main.py" ]