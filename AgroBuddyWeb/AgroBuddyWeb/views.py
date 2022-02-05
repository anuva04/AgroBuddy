from ast import parse
from django.shortcuts import render
import pickle
import os
import wikipedia
import requests
import environ

env = environ.Env()
environ.Env.read_env()

FLICKR_API_KEY = env('FLICKR_API_KEY')

# method to get wikipedia snippet
def wiki_snippet(search):
    try:
        result = wikipedia.summary(search, sentences = 3)
    except:
        return "Wrong Input"
    return result

# method to get image of a specific keyword
def get_image_url(search):
    search_by_key_url = 'https://www.flickr.com/services/rest/?method=flickr.photos.search&api_key='+FLICKR_API_KEY+'&tags='+search+'&format=json&nojsoncallback=1'
    response = requests.get(search_by_key_url).json()
    res = response['photos']['photo'][0]
    current_photo_url = 'https://farm'+str(res['farm'])+'.staticflickr.com/'+str(res['server'])+'/'+str(res['id'])+'_'+str(res['secret'])+'_n.jpg'
    return current_photo_url

#homepage view
def home(request):
    return render(request, 'index.html')

# method for generating predictions
def getPredictions(ph, moisture, humidity, temperature):
    model = pickle.load(open(os.path.dirname(os.path.realpath(__file__)) + '\crops.sav', "rb"))
    sc = pickle.load(open(os.path.dirname(os.path.realpath(__file__)) + '\scaler.sav', "rb"))
    prediction = model.predict(sc.transform([[ph, moisture, humidity, temperature]]))

    best_prediction = prediction[0]
    wikipedia_snippet = wiki_snippet(best_prediction)
    image_url = get_image_url(best_prediction)

    return [best_prediction.upper(), wikipedia_snippet, image_url]

# method for rendering result
def result(request):
    ph = float(request.GET['ph'])
    moisture = float(request.GET['moisture'])
    humidity = float(request.GET['humidity'])
    temperature = float(request.GET['temperature'])

    result = getPredictions(ph, moisture, humidity, temperature)

    return render(request, 'result.html', {'ph':ph, 'moisture':moisture, 'humidity':humidity, 'temp':temperature, 'result':result[0], 'wiki':result[1], 'image':result[2]})
    