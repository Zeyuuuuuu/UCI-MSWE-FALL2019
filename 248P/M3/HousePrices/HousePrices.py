import keras
import numpy as np
from keras.datasets import boston_housing
from keras import layers
from keras import models
from keras import backend as K
import matplotlib.pyplot as plt



(train_data, train_targets), (test_data, test_targets) =  boston_housing.load_data()
# train_data.shape
# test_data.shape
# train_targets

mean = train_data.mean(axis=0)
train_data -= mean
std = train_data.std(axis=0)
train_data /= std

test_data -= mean
test_data /= std



def build_model(n_layers,n_unit,act_func):
    # Because we will need to instantiate
    # the same model multiple times,
    # we use a function to construct it.
    model = models.Sequential()
    model.add(layers.Dense(n_unit, activation=act_func,
                           input_shape=(train_data.shape[1],)))
    for _ in range(n_layers-1):
      model.add(layers.Dense(n_unit, activation=act_func))
    model.add(layers.Dense(1))
    model.compile(optimizer='rmsprop', loss='mse', metrics=['mae'])
    return model


k = 4
num_val_samples = len(train_data) // k
num_epochs = 500

# Some memory clean-up
def cross_validation(n_layers,n_unit,act_func,index):
  K.clear_session()
  all_mae_histories = []
  for i in range(k):
      print('processing fold #', i)
      # Prepare the validation data: data from partition # k
      val_data = train_data[i * num_val_samples: (i + 1) * num_val_samples]
      val_targets = train_targets[i * num_val_samples: (i + 1) * num_val_samples]

      # Prepare the training data: data from all other partitions
      partial_train_data = np.concatenate(
          [train_data[:i * num_val_samples],
          train_data[(i + 1) * num_val_samples:]],
          axis=0)
      partial_train_targets = np.concatenate(
          [train_targets[:i * num_val_samples],
          train_targets[(i + 1) * num_val_samples:]],
          axis=0)

      # Build the Keras model (already compiled)
      model = build_model(n_layers,n_unit,act_func)
      # Train the model (in silent mode, verbose=0)
      history = model.fit(partial_train_data, partial_train_targets,
                          validation_data=(val_data, val_targets),
                          epochs=num_epochs, batch_size=1, verbose=0)
      mae_history = history.history['val_mean_absolute_error']
      all_mae_histories.append(mae_history)

  average_mae_history = [
      np.mean([x[i] for x in all_mae_histories]) for i in range(num_epochs)]
  best_epoch = average_mae_history.index(min(average_mae_history))
  print(best_epoch)

  # plt.plot(range(1, len(average_mae_history) + 1), average_mae_history)
  # plt.xlabel('Epochs')
  # plt.ylabel('Validation MAE')
  # plt.show()

  def smooth_curve(points, factor=0.9):
    smoothed_points = []
    for point in points:
      if smoothed_points:
        previous = smoothed_points[-1]
        smoothed_points.append(previous * factor + point * (1 - factor))
      else:
        smoothed_points.append(point)
    return smoothed_points

  smooth_mae_history = smooth_curve(average_mae_history[10:])
  plt.figure()
  plt.plot(range(1, len(smooth_mae_history) + 1), smooth_mae_history)
  plt.xlabel('Epochs')
  plt.ylabel('Validation MAE')
  # plt.show()
  plt.savefig('ex'+str(index+1)+'_validation_mae.png')
  return best_epoch

def train(n_epoch,n_layers,n_unit,act_func):
  # Get a fresh, compiled model.
  model = build_model(n_layers,n_unit,act_func)
  # Train it on the entirety of the data.
  history = model.fit(train_data, train_targets,
            epochs=n_epoch, batch_size=16, verbose=0)
  acc = history.history['mean_absolute_error']
  loss = history.history['loss']
  print("train: ",loss[-1],acc[-1])
  test_mse_score, test_mae_score = model.evaluate(test_data, test_targets)
  print('test: ',test_mse_score, test_mae_score)


config = [(2,64,'relu'),(1,64,'relu'),(3,64,'relu'),(2,32,'relu'),(2,128,'relu'),(2,64,'tanh')]

for i,(n_layers,n_unit,act_func) in enumerate(config):
  n_epoch = cross_validation(n_layers,n_unit,act_func,i)
  train(n_epoch,n_layers,n_unit,act_func)