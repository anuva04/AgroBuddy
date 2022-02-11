import pickle
import os

model = pickle.load(open(os.path.dirname(os.path.realpath(__file__)) + '\crops.sav', "rb"))
sc = pickle.load(open(os.path.dirname(os.path.realpath(__file__)) + '\scaler.sav', "rb"))