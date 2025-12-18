#!/usr/bin/env python
# coding: utf-8

# This is a notebook for an updated module 5 of ML Zoomcamp
# 
# The code is based on the modules 3 and 4. We use the same dataset: [telco customer churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)

# In[1]:


import pandas as pd
import numpy as np
import sklearn


# In[2]:


print(f'pandas=={pd.__version__}')
print(f'numpy=={np.__version__}')
print(f'sklearn=={sklearn.__version__}')


# In[3]:


from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression


# In[4]:


# Data preparation
data_url = 'https://raw.githubusercontent.com/ekhlebus/ml-zoomcamp/refs/heads/main/03-classification_churn_prediction/WA_Fn-UseC_-Telco-Customer-Churn.csv'

df = pd.read_csv(data_url)

df.columns = df.columns.str.lower().str.replace(' ', '_')

categorical_columns = list(df.dtypes[df.dtypes == 'object'].index)

for c in categorical_columns:
    df[c] = df[c].str.lower().str.replace(' ', '_')

df.totalcharges = pd.to_numeric(df.totalcharges, errors='coerce')
df.totalcharges = df.totalcharges.fillna(0)

df.churn = (df.churn == 'yes').astype(int)


# In[5]:


df.head(3)


# In[6]:


y_train = df.churn


# In[7]:


numerical = ['tenure', 'monthlycharges', 'totalcharges']

categorical = [
    'gender',
    'seniorcitizen',
    'partner',
    'dependents',
    'phoneservice',
    'multiplelines',
    'internetservice',
    'onlinesecurity',
    'onlinebackup',
    'deviceprotection',
    'techsupport',
    'streamingtv',
    'streamingmovies',
    'contract',
    'paperlessbilling',
    'paymentmethod',
]


# In[8]:


dv = DictVectorizer()

train_dict = df[categorical + numerical].to_dict(orient='records')
X_train = dv.fit_transform(train_dict)

model = LogisticRegression(solver='liblinear')
model.fit(X_train, y_train)


# Right now we have a problem: we have a tupple, two objects (dv and model) which we need to save and load separately and so on. It is not convinient.
# 
# Instead we can use a pipeline!

# In[9]:


from sklearn.pipeline import make_pipeline


# In[10]:


pipeline = make_pipeline(
    DictVectorizer(),
    LogisticRegression(solver='liblinear')
)


# In[11]:


train_dict = df[categorical + numerical].to_dict(orient='records')

pipeline.fit(train_dict, y_train)


# For now here we are using entire dataset (splitting and other steps were done in modules 3 and 4) and want to deploy the model.

# In[12]:


# Let's say this is the customer profile we want to use for prediction
customer = {
    'gender': 'male',
    'seniorcitizen': 0,
    'partner': 'no',
    'dependents': 'yes',
    'phoneservice': 'no',
    'multiplelines': 'no_phone_service',
    'internetservice': 'dsl',
    'onlinesecurity': 'no',
    'onlinebackup': 'yes',
    'deviceprotection': 'no',
    'techsupport': 'no',
    'streamingtv': 'no',
    'streamingmovies': 'no',
    'contract': 'month-to-month',
    'paperlessbilling': 'yes',
    'paymentmethod': 'electronic_check',
    'tenure': 6,
    'monthlycharges': 29.85,
    'totalcharges': 129.85
    }


# Let's make a prediction for this customer:

# In[13]:


# Turn the customer into a matrix that we can use for prediction
X = dv.transform(customer)


# In[14]:


# Predict the probability of churn for this customer
churn = model.predict_proba(X)[0, 1]
churn


# ## Saving the model
# 
# In order to use this model we need to save it

# In[15]:


import pickle


# In[16]:


## Previously we saved our model and dv into a file called model.bin using next code
# with open('model.bin', 'wb') as f_out:
#    pickle.dump((dv, model), f_out)    # saved as a tuple (two objects: dv and model)

# Now we will save the pipeline instead
with open('model.bin', 'wb') as f_out:
    pickle.dump(pipeline, f_out)    # saved as a single object (the pipeline) 


# In[17]:


# Now we can see that we have a new file called model.bin in our current directory
get_ipython().system('ls -lh')


# ## Load the model
# 
# Restart the kernel and load the model

# In[1]:


import pickle


# In[2]:


# we will load the model and dv from the file model.bin
with open('model.bin', 'rb') as f_in:
    pipeline = pickle.load(f_in)


# In[3]:


pipeline


# In[6]:


# Let's say this is the customer profile we want to use for prediction
customer = {
    'gender': 'male',
    'seniorcitizen': 0,
    'partner': 'no',
    'dependents': 'yes',
    'phoneservice': 'no',
    'multiplelines': 'no_phone_service',
    'internetservice': 'dsl',
    'onlinesecurity': 'no',
    'onlinebackup': 'yes',
    'deviceprotection': 'no',
    'techsupport': 'no',
    'streamingtv': 'no',
    'streamingmovies': 'no',
    'contract': 'month-to-month',
    'paperlessbilling': 'yes',
    'paymentmethod': 'electronic_check',
    'tenure': 6,
    'monthlycharges': 29.85,
    'totalcharges': 129.85
    }


churn = pipeline.predict_proba(customer)[0, 1]
print('prob of churning =', churn)


# In[5]:


if churn >= 0.5:
    print('send email with special offer to prevent churn')
else:
    print('no action needed')


# Now let's convert it to python script. For that we can run next code: 
# 
# ```
# jupyter nbconvert --to=script workshop-uv-fastpi.ipynb
# ```
# 
# Now workshop-uv-fastpi.ipynb converted into workshop-uv-fastpi.py script.

# 
