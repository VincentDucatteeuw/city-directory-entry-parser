from cdparser import Classifier

file = str(input("Path to data...: "))
model = str(input("Model (don't forget to add .pkg!)...: "))

classifier = Classifier.Classifier()
classifier.listen(file, model)

