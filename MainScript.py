import tensorflow as tf
import DataWorker
import Constants

x = tf.placeholder(tf.float32, [None, Constants.sequenceLength, DataWorker.numFeatures])
y = tf.placeholder(tf.float32, [None, Constants.sequenceLength, 1])
xTensors = tf.unstack(x, axis=1)   # [seqLength tensors of shape (batchSize, numFeatures)]
yTensors = tf.unstack(y, axis=1)

W = tf.Variable(tf.random_normal([Constants.numHidden, 1]))     # Weighted matrix
b = tf.Variable(tf.random_normal([1]))                          # Bias

# cells = [tf.contrib.rnn.BasicLSTMCell(Constants.numHidden, forget_bias=Constants.forgetBias) for _ in range(Constants.numLayers)]
# cell = tf.contrib.rnn.MultiRNNCell(cells)
cell = tf.contrib.rnn.BasicLSTMCell(Constants.numHidden)

outputs, finalState = tf.nn.static_rnn(cell, xTensors, dtype=tf.float32)
predictions = [tf.add(tf.matmul(output, W), b) for output in outputs]
predictions = tf.minimum(tf.maximum(predictions, 0), 1)                                 # Activation
mse = tf.losses.mean_squared_error(predictions=predictions, labels=yTensors)                   # Mean loss over entire batch
#
# multiplier = tf.constant(10 ** Constants.labelPrecision, dtype=y.dtype)
# roundedPredictions = tf.minimum(tf.round(predictions * multiplier) / multiplier, 1)
#
# accuracy = tf.reduce_mean(1 - tf.abs(y - roundedPredictions) / 1.0)                     # Accuracy over entire batch
# optimiser = tf.train.GradientDescentOptimizer(Constants.learningRate).minimize(mse)     # Backpropagation
#
# with tf.Session() as session:
#     session.run(tf.global_variables_initializer())
#     # #############################################
#     # TRAINING
#     # #############################################
#     for epoch in range(Constants.numEpochs):
#         print("***** EPOCH:", epoch + 1, "*****\n")
#         IDPointer, TSPointer = 0, 0         # Pointers to current ID and timestamp
#         epochComplete = False
#         batchNum = 0
#         while not epochComplete:
#             batchNum += 1
#             batchX, batchY, batchLabels, IDPointer, TSPointer, epochComplete = DataWorker.generateBatch(IDPointer, TSPointer)
#             dict = {x: batchX, y: batchY}
#             session.run(optimiser, dict)
#             if batchNum % Constants.printStep == 0 or epochComplete:
#                 batchLoss = session.run(mse, dict)
#                 batchAccuracy = session.run(accuracy, dict)
#                 print("Iteration:", batchNum)
#                 print("Label:\t ", session.run(y[-1][0], dict))
#                 print("Pred:\t ", session.run(roundedPredictions[-1][0], dict))
#                 print("Loss:\t ", batchLoss)
#                 print("Accuracy:", str("%.2f" % (batchAccuracy * 100) + "%\n"))
#
#     # #############################################
#     # TESTING
#     # #############################################
#     testX, testY, testLabels, _, _, _ = DataWorker.generateTestBatch()
#     testAccuracy = session.run(accuracy, {x: testX, y: testY})
#     print("Testing Accuracy:", str("%.2f" % (testAccuracy * 100) + "%"))