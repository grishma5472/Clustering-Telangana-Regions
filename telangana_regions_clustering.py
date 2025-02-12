# -*- coding: utf-8 -*-
"""Telangana regions clustering.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1PoqRKwwfWdJMaMrvDCdM9kgOLDA4FvOh
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

df=pd.read_csv('clustering_data.csv')
df.shape
df.head()

#Extracting Home State i.e., Telangana State's data
hs_data=df[df.StateName=='TELANGANA']

hs_data.head()

hs_data.tail()

hs_data.shape

#Visualising the geographical location using longitude, latitude data

fig=px.scatter_geo(hs_data,lat='Latitude',lon='Longitude',hover_name="StateName")
fig.update_layout(title='Telangana Area',title_x=0.5)
fig.show()
#Leave alone Telanagana, many of the coordinates do not even lie in India.

"""DATA PREPROCESSING"""

#data preprocessing
hs_data.info()

missing_values=hs_data.isnull().sum()
missing_values[0:11]
#There are a lot of missing values

#convert datatype of lat, long to float
hs_data['Latitude']=hs_data['Latitude'].astype(float)
hs_data['Longitude']=hs_data['Longitude'].astype(float)
hs_data.info()

hs_data=hs_data.dropna()
missing_values=hs_data.isnull().sum()
missing_values[0:11]

#We have used interpolation to handle missing values
#let us remove outliers
hs_data.describe()

max_lat=19.783  #These can be set through domain knowledge

min_lat=15.767

max_long=81.717

min_long=77.267

hs_data=hs_data[(hs_data['Latitude']<=max_lat)&(hs_data['Latitude']>=min_lat)&(hs_data['Longitude']<=max_long)&(hs_data['Longitude']>=min_long)]
hs_data.info()

plt.scatter(hs_data['Longitude'],hs_data['Latitude'])

fig=px.scatter_geo(hs_data,lat='Latitude',lon='Longitude',hover_name="StateName")
fig.update_layout(title='Telangana Area',title_x=0.5)
fig.show()

X=np.array(hs_data[['Longitude','Latitude']])
def kmeans(data, k):
  centroids = X[np.random.choice(X.shape[0], k, replace=False)]
  for _ in range(100):
    labels = np.argmin(np.linalg.norm(X[:, np.newaxis] - centroids, axis=2), axis=1)
    centroids = np.array([np.mean(X[labels == i], axis=0) for i in range(k)])
  return labels, centroids

"""CLUSTERING BASED ON NUMBER OF DISTRICTS"""

#To find number of districts
num=len(pd.unique(hs_data['District']))
print("Number of districts:", num)

labels, centroids = kmeans(X, 33)
plt.scatter(X[:,0],X[:,1],c = labels)

#From here it is clear that many pincodes in Hyderabad city region, and in districts near Khammam are not availble