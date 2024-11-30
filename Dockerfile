FROM python:3.9-slim

WORKDIR /usr/src/app

COPY src/rocrateValidator/ rocrateValidator/

RUN echo "requests\nrocrate" > requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY src/cli.py .

ENTRYPOINT ["python", "./cli.py"]
