import numpy
import scipy.special

class nn:
    def __init__(self, inputNodes, hiddenNodes, outputNodes, learningRate):
        self.iNodes = inputNodes
        self.hNodes = hiddenNodes
        self.oNodes = outputNodes
        self.lr = learningRate
        self.wih = (numpy.random.rand(self.hNodes, self.iNodes)-0.5)
        self.who = (numpy.random.rand(self.oNodes, self.hNodes)-0.5)

        self.activationFunction = lambda x:scipy.special.expit(x)
       
    def train(self,inputs_list, targets_list):
        inputs = numpy.array(inputs_list, ndmin = 2).T
        targets = numpy.array(targets_list, ndmin = 2).T

        hidden_inputs = numpy.dot(self.wih, inputs)
        hidden_outputs = self.activationFunction(hidden_inputs)

        final_inputs = numpy.dot(self.who, hidden_outputs)
        final_outputs = self.activationFunction(final_inputs)


        output_errors = targets - final_outputs
        hidden_errors = numpy.dot(self.who.T, output_errors)
        self.who += self.lr * numpy.dot((output_errors*final_outputs*(1.0 - final_outputs)), numpy.transpose(hidden_outputs))
        self.wih += self.lr * numpy.dot((hidden_errors*hidden_outputs*(1.0 - hidden_outputs)), numpy.transpose(inputs))


    def query(self, inputs_list):
        inputs = numpy.array(inputs_list, ndmin = 2,dtype=numpy.int64).T

        hidden_inputs = numpy.dot(self.wih, inputs)
        hidden_outputs = self.activationFunction(hidden_inputs)

        final_inputs = numpy.dot(self.who, hidden_outputs)
        final_outputs = self.activationFunction(final_inputs)

        return final_outputs
