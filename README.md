# Iris Classification API

[![Docker smoke test](https://github.com/dw733/iris-classification-api/actions/workflows/docker.yml/badge.svg)](https://github.com/dw733/iris-classification-api/actions/workflows/docker.yml)

I wanted to make a model I could use outside a notebook. This is the portfolio version of my Iris project. It takes four flower measurements as JSON and sends back the predicted species.

I used a scikit-learn pipeline that scales the inputs and fits logistic regression. On a fixed 80/20 split, it predicted **28 of 30 held-out examples correctly (93.3%)**. That’s a small test set, so I use the result as a quick check. The API part is what I wanted to practice here.

## Try it with Docker

```bash
docker build -t iris-api .
docker run --rm -p 127.0.0.1:8000:8000 iris-api
```

In another terminal, check the API and send a prediction.

```bash
curl http://127.0.0.1:8000/health
curl -X POST http://127.0.0.1:8000/predict -H 'Content-Type: application/json' -d '{"sepal_length_cm":5.1,"sepal_width_cm":3.5,"petal_length_cm":1.4,"petal_width_cm":0.2}'
```

In Windows PowerShell, try the same prediction with:

```powershell
$measurements = @{
    sepal_length_cm = 5.1
    sepal_width_cm = 3.5
    petal_length_cm = 1.4
    petal_width_cm = 0.2
} | ConvertTo-Json
Invoke-RestMethod -Uri http://127.0.0.1:8000/predict -Method Post -ContentType 'application/json' -Body $measurements
```

The JSON prediction response is `{"species":"setosa"}`. Send all four named measurements as positive numbers in centimetres. If a measurement is missing or invalid, the API returns an error message with status 400.

## Run it with Python

Use Python 3.12 in an active virtual environment.

```bash
python -m pip install -r requirements.txt
python -m unittest -v
python model.py
python -m flask --app app:create_app run --port 8000
```

I keep the [model training](model.py) and [API routes](app.py) in separate files. The API reads the measurements by name and puts them in the same order every time, even if the request sends the keys in a different order. The [tests](test_api.py) check that behavior along with a few bad requests.
