from cdparser import Classifier

# /home/bavercru/Documents/Visual Code - workspace/CRF/data/ghent-city-directories/wegwijzer-1913-entries-sample.txt
# /home/bavercru/Documents/Visual Code - workspace/CRF/data/ghent-city-directories/wegwijzer-labeled-p533-543-training.csv
# /home/bavercru/Documents/Visual Code - workspace/CRF/data/ghent-city-directories/clean-wegwijzer.csv
classifier = Classifier.Classifier()
trainingdata = str(input("Path to trainingdata...: "))
classifier.load_training(trainingdata)
classifier.train(input("Name of the model...: "))