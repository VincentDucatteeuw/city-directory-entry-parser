from cdparser import Classifier

classifier = Classifier.Classifier()
trainingdata = str(input("Path to trainingdata...: "))
classifier.load_training(trainingdata)
classifier.train(input("Name of the model...: "))

# /home/bavercru/Documents/Visual Code - workspace/CRF/data/ghent-city-directories/wegwijzer-labeled-p533-543-training.csv