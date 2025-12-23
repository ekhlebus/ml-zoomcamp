#!/usr/bin/env python
# coding: utf-8

import pickle

#from typing import Dict, Any

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, Field, ConfigDict, conint, confloat
from typing import Literal


#requests
# Here we define all values that supposed to be sent by user

class Customer(BaseModel):
    gender: Literal["male", "female"]
    seniorcitizen: Literal[0, 1]

    partner: Literal["yes", "no"]
    dependents: Literal["yes", "no"]

    phoneservice: Literal["yes", "no"]
    multiplelines: Literal["yes", "no", "no_phone_service"]

    internetservice: Literal["fiber_optic", "dsl", "no"]
    onlinesecurity: Literal["yes", "no", "no_internet_service"]
    onlinebackup: Literal["yes", "no", "no_internet_service"]
    deviceprotection: Literal["yes", "no", "no_internet_service"]
    techsupport: Literal["yes", "no", "no_internet_service"]
    streamingtv: Literal["yes", "no", "no_internet_service"]
    streamingmovies: Literal["yes", "no", "no_internet_service"]

    contract: Literal["month-to-month", "one_year", "two_year"]
    paperlessbilling: Literal["yes", "no"]

    paymentmethod: Literal[
        "electronic_check",
        "mailed_check",
        "bank_transfer_(automatic)",
        "credit_card_(automatic)",
    ]

    tenure: conint(ge=0)  # tenure should be non-negative integer
    monthlycharges: confloat(ge=0)  # monthlycharges should be non-negative float
    totalcharges: confloat(ge=0)  # totalcharges should be non-negative float


#responce
class PredictResponse(BaseModel):
    churn_probability: float
    churn: bool


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
@app.post("/predict")  # This function will be accessible at address /predict using POST method
def predict(customer: Customer) -> PredictResponse:
    churn = predict_single(customer.dict())
    return PredictResponse(
        churn_probability = churn,
        churn=bool(churn >= 0.5)
    )

# We are using "__main__" top-level script environment to run the app
if __name__ == "__main__":
    # Run the app on port 9696 at localhost
    uvicorn.run(app, host='0.0.0.0', port=9696) 
