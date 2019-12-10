from django.shortcuts import render
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import Imputer
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from django.core.files.storage import FileSystemStorage
from django.conf import settings
# Create your views here.
def insurance(request):
    try:
        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)

            dataset = pd.read_csv('C:\\Users\\ajink\\Downloads\\policy(1).csv')
            X=dataset.iloc[:,[0,1]].values
            y=dataset.iloc[:,2].values
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)
            model=DecisionTreeClassifier()
            model.fit(X_train,y_train)
            y_pred = model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            age = int(request.POST.get('age'))
            savings = int(request.POST.get('savings'))
            # children = int(request.POST.get('children'))
            # smoker = int(request.POST.get('smoker'))
            # region = int(request.POST.get('region'))
            # sex = int(request.POST.get('sex'))
            prediction = model.predict([[age, savings]])
            print(prediction)

            return render(request, 'insurance.html', {'uploaded_file_url': uploaded_file_url, 'accuracy': accuracy, 'prediction': prediction})
        return render(request, 'insurance.html')
    except:
        return render(request, 'insurance.html', {'error': 'Please Select A File'})
