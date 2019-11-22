import keras
from keras.datasets import imdb
import numpy as np
from keras import models
from keras import layers
from keras import optimizers
from keras import losses
from keras import metrics
import matplotlib.pyplot as plt

# print(keras.__version__)


(train_data, train_labels), (test_data, test_labels) = imdb.load_data(num_words=10000)

# print(train_data[0])
# print(train_labels[0])
# print(max([max(sequence) for sequence in train_data]))

# word_index is a dictionary mapping words to an integer index
word_index = imdb.get_word_index()
# We reverse it, mapping integer indices to words
reverse_word_index = dict([(value, key) for (key, value) in word_index.items()])
# We decode the review; note that our indices were offset by 3
# because 0, 1 and 2 are reserved indices for "padding", "start of sequence", and "unknown".
decoded_review = ' '.join([reverse_word_index.get(i - 3, '?') for i in train_data[0]])
# print(decoded_review)


def vectorize_sequences(sequences, dimension=10000):
    # Create an all-zero matrix of shape (len(sequences), dimension)
    results = np.zeros((len(sequences), dimension))
    for i, sequence in enumerate(sequences):
        results[i, sequence] = 1.  # set specific indices of results[i] to 1s
    return results

# Our vectorized training data
x_train = vectorize_sequences(train_data)
# Our vectorized test data
x_test = vectorize_sequences(test_data)
# print(x_train[0])

# Our vectorized labels
y_train = np.asarray(train_labels).astype('float32')
y_test = np.asarray(test_labels).astype('float32')

def train(n_layers,n_unit,act,loss_func,index):
    model = models.Sequential()
    model.add(layers.Dense(n_unit, activation=act, input_shape=(10000,)))
    for _ in range(n_layers-1):
        model.add(layers.Dense(n_unit, activation=act))

    model.add(layers.Dense(1, activation='sigmoid'))
    # model.compile(optimizer='rmsprop',
    #               loss='binary_crossentropy',
    #               metrics=['accuracy'])
    # model.compile(optimizer=optimizers.RMSprop(lr=0.001),
    #               loss='binary_crossentropy',
    #               metrics=['accuracy'])


    model.compile(optimizer=optimizers.RMSprop(lr=0.001),
                loss=loss_func,
                metrics=[metrics.binary_accuracy])

    x_val = x_train[:10000]
    partial_x_train = x_train[10000:]

    y_val = y_train[:10000]
    partial_y_train = y_train[10000:]

    history = model.fit(partial_x_train,
                        partial_y_train,
                        epochs=20,
                        batch_size=512,
                        validation_data=(x_val, y_val))

    history_dict = history.history
    print(history_dict.keys())


    acc = history.history['binary_accuracy']
    val_acc = history.history['val_binary_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']

    epochs = range(1, len(acc) + 1)
    plt.figure()

    # # "bo" is for "blue dot"
    plt.plot(epochs, loss, 'bo', label='Training loss')
    # b is for "solid blue line"
    plt.plot(epochs, val_loss, 'b', label='Validation loss')
    plt.title('Training and validation loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()

    plt.savefig('ex'+str(index)+'_loss.png')

    plt.figure()


    plt.plot(epochs, acc, 'bo', label='Training acc')
    plt.plot(epochs, val_acc, 'b', label='Validation acc')
    plt.title('Training and validation accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.savefig('ex'+str(index)+'_acc.png')

    # model = models.Sequential()
    # model.add(layers.Dense(16, activation='relu', input_shape=(10000,)))
    # model.add(layers.Dense(16, activation='relu'))
    # model.add(layers.Dense(1, activation='sigmoid'))

    # model.compile(optimizer='rmsprop',
    #               loss='binary_crossentropy',
    #               metrics=['accuracy'])

    # model.fit(x_train, y_train, epochs=4, batch_size=512)
    results = model.evaluate(x_test, y_test)
    print(results)
    # model.predict(x_test)

config = [(2,64,'relu',losses.binary_crossentropy),
(1,64,'relu',losses.binary_crossentropy),
(3,64,'relu',losses.binary_crossentropy),
(2,32,'relu',losses.binary_crossentropy),
(2,128,'relu',losses.binary_crossentropy),
(2,64,'relu',losses.binary_crossentropy),
(2,64,'relu',losses.mean_squared_error),
(2,64,'tanh',losses.binary_crossentropy)]

for i,(n_layers,n_unit,act,loss_func) in enumerate(config):
    train(n_layers,n_unit,act,loss_func,i)