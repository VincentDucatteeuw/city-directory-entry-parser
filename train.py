from cdparser import Classifier

classifier = Classifier.Classifier()
trainingdata = str(input("Path to trainingdata...: "))
classifier.load_training(trainingdata)
classifier.train(input("Name of the model...: "))