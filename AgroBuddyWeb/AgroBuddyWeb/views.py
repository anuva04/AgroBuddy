from django.shortcuts import render
import wikipedia
import requests
import environ
from .__init__ import model, sc

# retrieving environment variables
env = environ.Env()
environ.Env.read_env()
FLICKR_API_KEY = env('FLICKR_API_KEY')
PIXABAY_API_KEY = env('PIXABAY_API_KEY')

# method to get wikipedia snippet
def wiki_snippet(search):
    try:
        result = wikipedia.summary(search, sentences = 3)
    except:
        try:
            result = wikipedia.summary(search, sentences = 3)
        except:
            return "Please Click"
    return result

# method to get image of a specific keyword using Flickr API
def get_image_url_flickr(search):
    search_by_key_url = 'https://www.flickr.com/services/rest/?method=flickr.photos.search&api_key='+FLICKR_API_KEY+'&tags='+search+'&format=json&nojsoncallback=1'
    response = requests.get(search_by_key_url).json()
    res = response['photos']['photo'][0]
    current_photo_url = 'https://farm'+str(res['farm'])+'.staticflickr.com/'+str(res['server'])+'/'+str(res['id'])+'_'+str(res['secret'])+'_n.jpg'
    return current_photo_url

# method to get image of a specific keyword using pixabay API
def get_image_url_pixabay(search):
    search_by_key_url = 'https://pixabay.com/api/?key='+PIXABAY_API_KEY+'&q='+search+'&image_type=photo'
    response = requests.get(search_by_key_url).json()
    current_photo_url = response['hits'][1]['webformatURL']
    return current_photo_url

#homepage view
def home(request):
    return render(request, 'index.html')

# method for generating predictions
def getPredictions(ph, moisture, humidity, temperature):
    prediction = model.predict(sc.transform([[ph, moisture, humidity, temperature]]))

    best_prediction = prediction[0]
    wikipedia_snippet = wiki_snippet(best_prediction)
    image_url = get_image_url_pixabay(best_prediction)

    return [best_prediction.upper(), wikipedia_snippet, image_url]

# method for rendering result
def result(request):
    ph = float(request.GET['ph'])
    moisture = float(request.GET['moisture'])
    humidity = float(request.GET['humidity'])
    temperature = float(request.GET['temperature'])

    result = getPredictions(ph, moisture, humidity, temperature)

    return render(request, 'result.html', {'ph':ph, 'moisture':moisture, 'humidity':humidity, 'temp':temperature, 'result':result[0], 'wiki':result[1], 'image':result[2]})
    