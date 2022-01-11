from django.shortcuts import render
import pickle
import os

#homepage view
def home(request):
    return render(request, 'index.html')

# method for generating predictions
def getPredictions(ph, moisture, humidity, temperature):
    model = pickle.load(open(os.path.dirname(os.path.realpath(__file__)) + '\crops.sav', "rb"))
    sc = pickle.load(open(os.path.dirname(os.path.realpath(__file__)) + '\scaler.sav', "rb"))
    prediction = model.predict(sc.transform([[ph, moisture, humidity, temperature]]))

    return prediction

# method for rendering result
def result(request):
    ph = float(request.GET['ph'])
    moisture = float(request.GET['moisture'])
    humidity = float(request.GET['humidity'])
    temperature = float(request.GET['temperature'])

    result = getPredictions(ph, moisture, humidity, temperature)

    return render(request, 'result.html', {'result':result})
    