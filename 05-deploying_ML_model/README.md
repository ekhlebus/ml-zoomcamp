# Deploying Machine Learning Models

This repository contains info about saving, loading, and deployment churn prediction model.

Our model is still in Jupyter notebook. Now let's deploy it - save it and use it.

“Deploy the model” means taking a trained machine-learning model and making it available for real-world use, so that new data can be sent to it and it can return predictions.

This usually involves putting the model into a production environment—such as a web service, API, cloud platform, or application—so that users or other systems can call it to get predictions.

## Files in this repo:

* **05-train-churn-model.ipynb** Jupyten notebook with code for saving and loading model.

* **train_churn_prediction.py** Python script from Jupyten notebook above for training churn prediction model. Running this script will train and save the model into **churn_prediction_model_C=1.bin**

* **churn_prediction.py** Python script from Jupyten notebook above for using previously saved model and making churn prediction.

* **ping.py** Python script for making simple ping-pong app as web service using Flask.
To run this script: python ping.py. After running we can see something like this:
![running_ping](images/running_ping.PNG)

Query it with 'curl' and browser.

* **churn_prediction_web-service.py** Python script for wrapping the **churn_prediction.py** script into a Flask app (serving the churn prediction model with Flask). Query it with 'requests'.