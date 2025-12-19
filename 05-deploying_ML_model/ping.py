# Here we are turning ping function into a web service using FastAPI

import uvicorn
from fastapi import FastAPI

# Define the application using FastAPI
app = FastAPI(title='ping')

# Add decorator to add extra functionality to ping function (here it allows us to turn function into web service)
@app.get("/ping")  # This function will be accessible at address /ping using GET method (we can use browser to access it)

# Making ping function
# It is not just a regular function actually, it is a web service endpoint.
# It means that we can access this function using URL
def ping():
    return "PONG"

# We are using "__main__" top-level script environment to run the app
if __name__ == "__main__":
    # Run the app on port 9696 at localhost
    uvicorn.run(app, host='0.0.0.0', port=9696) 