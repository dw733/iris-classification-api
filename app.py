"""Serve Iris species predictions through a small Flask API."""

import math

from flask import Flask, jsonify, request

from model import FEATURES, fit_classifier


def create_app():
    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = 4096
    classifier, species, _, _ = fit_classifier()

    @app.get("/health")
    def health():
        return jsonify(status="ok")

    @app.post("/predict")
    def predict():
        if not request.is_json:
            return jsonify(error="Use Content-Type: application/json."), 415

        payload = request.get_json(silent=True)
        if not isinstance(payload, dict) or set(payload) != set(FEATURES):
            return jsonify(error="Send exactly these four measurements.", fields=FEATURES), 400

        # Read features in the same order the model used to train.
        measurements = []
        for feature in FEATURES:
            value = payload[feature]
            try:
                number = float(value) if type(value) in (int, float) else math.nan
            except OverflowError:
                number = math.nan
            if not math.isfinite(number) or not 0 < number <= 100:
                return jsonify(error=f"{feature} must be a number greater than 0 and at most 100 cm."), 400
            measurements.append(number)

        prediction = classifier.predict([measurements])[0]
        return jsonify(species=str(species[prediction]))

    return app
