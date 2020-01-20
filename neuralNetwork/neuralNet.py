import tensorflow as tf
import numpy as np
# import preprocess

class MODEL():
    def load_data(self):
        print("Loading Data...")
        X_train, X_test, y_train, y_test, headers = preprocess.load_data()
        self.X_train = np.array(X_train)
        self.X_test = np.array(X_test)
        self.y_train = np.array(y_train)
        self.y_test = np.array(y_test)
        self.headers = headers

    def init_model(self):
        print("Initializing Model...")
        # Create model
        self.model = tf.keras.models.Sequential()

        # Setup the model layers: 
        # what is the input shape? Experiment with different activation types
        # input layer
        self.model.add(tf.keras.layers.Dense(7, input_dim=27, activation = "softmax"))
        # LSTM layer
        self.model.add(LSTM(64, return_sequences=False, dropout=0.1, recurrent_dropout=0.1))
        # Fully connected layer
        self.model.add(Dense(64, activation="softmax"))
        # output layer
        self.model.add(Dense(7, activation="softmax"))


        # Compile model
        # Experiment with different loss types
        self.model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    def train_model(self, epochs):
        print("Training Model...")
        self.history = self.model.fit(
            self.X_train, 
            self.y_train,
            batch_size=self.BATCH_SIZE,
            epochs=epochs, 
            verbose=1,
            validation_data=(self.X_test, self.y_test)
        )

    def test_model(self):
        score = self.model.evaluate(self.X_test, self.y_test, verbose=0)
        print()
        print("Loss:      {:.4f}".format(score[0]))
        print("Accuracy:  {:.2f}%".format(score[1]*100))

    def analyze_weights(self):
        last_weights = [1.0]
        for layer in self.model.layers[::-1]:
            weights, bias = layer.get_weights()
            sums = np.zeros(weights.shape[0])
            for i in range(weights.shape[0]):
                sums[i] += np.dot(weights[i], last_weights)
            last_weights = sums
        return np.abs(last_weights)

    def feature_importance(self):
        last_weights = self.analyze_weights()
        print("\nFeature Importance:")
        relevance = [[y, x] for y, x in sorted(zip(last_weights,self.headers))][::-1]
        for i in range(len(relevance)):
            space = " "*(30 - len(str(relevance[i][1])))
            print("{}{}{:.4f}".format(relevance[i][1], space, relevance[i][0]))

    def __init__(self, batch=50):
        self.BATCH_SIZE = batch

def main():
    model = MODEL()
    model.load_data()
    model.init_model()
    epochs = 100
    model.train_model(epochs)
    model.test_model()
        
if __name__ == '__main__':
	main()
