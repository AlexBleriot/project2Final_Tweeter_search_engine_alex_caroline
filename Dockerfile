FROM python:3.6

WORKDIR /app

RUN mkdir ./mlsample

RUN mkdir ./mlsample/model

ENV MODEL_DIR=/app/mlsample/model

ENV MODEL_FILE=/model.joblib

ENV METADATA_FILE=metadata.json

ENV FLASK_APP=app.py

COPY requirements.txt .

COPY tweets.csv .

RUN pip install -r requirements.txt

COPY . .

RUN python model.py

EXPOSE 5000

CMD ["python", "app.py"]
