# Deploying Machine Learning Models

This repository contains info about saving, loading, and deployment churn prediction model.

**Deploy the model** means taking a trained machine-learning model and making it available for real-world use, so that new data can be sent to it and it can return predictions.

This usually involves putting the model into a production environment—such as a web service, API, cloud platform, or application—so that users or other systems can call it to get predictions.

## Files in this repo:

* **05-train-churn-model.ipynb**
    Jupyten notebook with code for saving and loading model.

* **train.py**
    Python script from Jupyten notebook above for training churn prediction model. Running this script will train and save the model into **churn_prediction_model_C=1.bin**

* **churn_prediction.py**
    Python script from Jupyten notebook above for using previously saved model and making churn prediction.

* **ping.py**
    Python script for making simple ping-pong app as web service using Flask. After running this script (python ping.py) we can see something like below with address where it is running:
![running_ping](https://github.com/ekhlebus/ml-zoomcamp/blob/main/05-deploying_ML_model/images/running_ping.PNG)

    To use the service, query it from the terminal using `curl`:

    ```bash
    curl http://0.0.0.0:9696/ping
    ```
    Or open it in a browser: http://localhost:9696/ping

* **predict.py**
    Python script for wrapping the **churn_prediction.py** script into a Flask app (serving the churn prediction model with Flask).

   To communicate with this web service we can use Jupyter notebook. Code for that is in the file **05-train-churn-model.ipynb**, section "Making requests".
   
   ⚠️ Since we are running the Flask in debug mode, every changes which are made in churn_prediction_web-service.py file during running our web service are detected. 
   In production deployment we need to use **WSGI server** instead of plain Flask.

   * As an example of WSGI server we can use `gunicorn` on MacOC or Linux (gunicorn does not support Windows):

       ```bash
        gunicorn --bind 0.0.0.0:9696 predict:app
        ```
        In this case the next part of **predict.py** script will not be executed, because it is in if statement, and here we will not get warnings since not it is in production mode (no debug mode): 
        ```bash
        if __name__ == "__main__":
        app.run(debug=True, host='0.0.0.0', port=9696)
        ```
    * On Windows we can use an alternative, running in cmd terminal something like `waitress` (https://www.devdungeon.com/content/run-python-wsgi-web-app-waitress):

        ```bash
        pip install waitress
    
        waitress-serve --listen=0.0.0.0:9696 predict:app 
        ```
        Be sure that you have files **predict.py** and **churn_prediction_model_C=1.bin** in the folder where you are running `waitress`.

        To get prediction run **predict-test.py** in another cmd terminal. If `app.run(debug=True)` cause blocking behavior, hanging requests, then try to remove or comment out this block from **predict.py** file.


* **Pipfile** and **Pipfile.lock** 
Files for virtual environments. In _Pipfile_ we an see the libraries we installed. In _Pipfile.lock_ we can see that each library with its installed version is named and a hash file is there to reproduce if we move the environment to another machine.

    To install the libraries we want for our project in the virtual environment, use the command:
    
    ```
    pipenv install numpy scikit-learn==0.24.1 flask
    ```
    
    If we want to run the project in another machine, we can easily install the libraries we want with the command ```pipenv install```. This command will look into _Pipfile_ and _Pipfile.lock_ to install the libraries with specified version.

    After installing the required libraries we can run the project in the virtual environment with ```pipenv shell``` command. This will go to the virtual environment's shell and then any command we execute will use the virtual environment's libraries. 

* **Dockerfile** specifies what kind of things we want to do inside the container, what we want to put and run there.
We can find python tags on Docker hub which contains all the images of python: https://hub.docker.com/_/python.

   To run some specific image use code below and get python terminal:
   ```
   docker run -it --rm python:3.8.12-slim  # -it means that we want access to the terminal
   ```

   To go inside ```python:3.8.12-slim``` image we can access its Linux terminal using: 
   ```
   docker run -it --rm --entrypoint=bash python:3.8.12-slim 
   ```
   Here we can do whatever we want and it will be isolated from the other system. Everything what we want to do inside this Docker image we can define in _Dockerfile_.

   To build container using instructions from _Dockerfile_ from current directory:
   ```   
   docker build -t zoomcamp-test .
   ```
   After building we can run resulted image instead of running ```python:3.8.12-slim``` like we did before:
   ```
   docker run -it --rm -p 9696:9696 zoomcamp-test
   ```
