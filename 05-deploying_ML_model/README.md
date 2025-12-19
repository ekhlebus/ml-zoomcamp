# Deploying Machine Learning Models

This repository contains info about saving, loading, and deployment churn prediction model using FastAPI.

**Deploy the model** means taking a trained machine-learning model and making it available for real-world use, so that new data can be sent to it and it can return predictions.

This usually involves putting the model into a production environment—such as a web service, API, cloud platform, or application—so that users or other systems can call it to get predictions.

## Files in this repo:

* **workshop-uv-fastapi.ipynb**
    Jupyten notebook from updated workshop with code for saving and loading model, in this notebook dv and model saved as pipeline. Based on this notebook file **workshop-uv-fastapi.py** created, from this file we will do two files: **train.py** and **predict.py**.

* **ping.py**
    Python script for making simple ping-pong app as web service using FastAPI. We can open it in a browser: http://localhost:9696/ping.

    FastAPI has nice feature! Look at http://localhost:9696/docs and see what functions/endpoints we have in our application. Also, there we can see the description of our function and we can "Try it out" there.

* **predict.py**
    Python script for wrapping the **workshop-uv-fastapi.py** script into a FastAPI app (serving the churn prediction model with FastAPI).

    There is a way to reload it every time we change the code. This is a function to watch the changes (we will not need to stop and start the server every each change):
    ```
    uvicorn predict:app --host 0.0.0.0 --port 9696 --reload
    ```
    Now we can go to http://localhost:9696/docs and input customer in **json format** (double quotes):
    
    ![running_prediction_as_docs_in_browser](https://github.com/ekhlebus/ml-zoomcamp/blob/main/05-deploying_ML_model/images/churn-prediction_FastAPI_localhost-9696-docs.PNG)

     execute and see prediction:

     ![running_prediction_execution_as_docs_in_browser](https://github.com/ekhlebus/ml-zoomcamp/blob/main/05-deploying_ML_model/images/churn-prediction_FastAPI_localhost-9696-docs-execution.PNG)

    And conviniently the execution gives us the ```curl``` command. We can copy it and instead using it in browser, we can use it in command line.

* **marketing.py**
    Python script for making requests. Works only if web service is running (running ```python predict.py```).