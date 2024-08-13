from cdparser import Classifier
import argparse

file = str(input("Path to data...: "))
file = str(input("Model...: "))

classifier = Classifier.Classifier()
classifier.listen(file)
# /home/bavercru/Documents/Visual Code - workspace/CRF/data/ghent-city-directories/wegwijzer-labeled-p533-543-training.csv