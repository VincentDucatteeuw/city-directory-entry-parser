from cdparser import Classifier

file = str(input("Path to data...: "))
model = str(input("Model...: "))

file = '/home/bavercru/Documents/Visual Code - workspace/CRF/data/ghent-city-directories/wegwijzer-1913-entries-sample.txt'
model = 'test.pkg'

classifier = Classifier.Classifier()
classifier.listen(file, model)
# /home/bavercru/Documents/Visual Code - workspace/CRF/data/ghent-city-directories/wegwijzer-labeled-p533-543-training.csv

