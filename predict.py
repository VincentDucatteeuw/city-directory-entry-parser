from cdparser import Classifier

file = str(input("Path to data...: "))
model = str(input("Model...: "))

classifier = Classifier.Classifier()
classifier.listen(file, model)

