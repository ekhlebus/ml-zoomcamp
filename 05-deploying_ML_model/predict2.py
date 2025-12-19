#!/usr/bin/env python
# coding: utf-8

import pickle

# Load the model from the file model.bin
with open('model.bin', 'rb') as f_in:
    pipeline = pickle.load(f_in)

# Now we need to get customer data through request
def predict_single(customer):
    result = pipeline.predict_proba(customer)[0, 1]
    return float(result)


def predict(customer):
    churn = predict_single(customer)
    return {
        'churn_probability': churn,
        'churn': bool(churn >= 0.5)
    }

