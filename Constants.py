import os

# Current dir
wd = os.path.dirname(os.path.realpath(__file__))
dataDir = wd + '/Data/'
defaultFile = dataDir + 'train.h5'

sequenceLength = 25
batchSize = 100
numEpochs = 50
numLayers = 4
numHidden = 100
initialLearningRate = 0.001
forgetBias = 1.0
dropoutRate = 0.0
trainingPercentage = 0.8
printStep = 50

years = 5
