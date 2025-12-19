#!/usr/bin/env python
# coding: utf-8

import pickle

from typing import Dict, Any

import uvicorn
from fastapi import FastAPI

# Define the application using FastAPI
app = FastAPI(title='churn-prediction')

# Load the model from the file model.bin
with open('model.bin', 'rb') as f_in:
    pipeline = pickle.load(f_in)

# Function to make predictions, here we need to get customer data through request
def predict_single(customer):
    result = pipeline.predict_proba(customer)[0, 1]
    return float(result)


# Add decorator to add extra functionality to ping function (here it allows us to turn function into web service)
@app.post("/predict2")  # This function will be accessible at address /predict using POST method
def predict(customer: Dict[str, Any]):
    churn = predict_single(customer)
    return {
        'churn_probability': churn,
        'churn': bool(churn >= 0.5)
    }

# We are using "__main__" top-level script environment to run the app
if __name__ == "__main__":
    # Run the app on port 9696 at localhost
    uvicorn.run(app, host='0.0.0.0', port=9696) 
