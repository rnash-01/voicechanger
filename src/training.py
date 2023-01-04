# %% [markdown]
# ### Import modules

# %%
import tensorflow as tf

# from https://medium.com/ibm-data-ai/memory-hygiene-with-tensorflow-during-model-training-and-deployment-for-inference-45cf49a15688
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    for gpu in gpus:
        print(str(gpu))
        tf.config.experimental.set_virtual_device_configuration(gpu,[tf.config.experimental.VirtualDeviceConfiguration(memory_limit=4096)])


import tensorflow.keras as keras
from keras import layers
import numpy as np
from dataset import *

# %% [markdown]
# #### GPU config

# %% [markdown]
# ### Create dataset from test audio file
# 

# %%
xf, X, spec_params = create_dataset('audio/training_audio.wav', 2, 0.5)
X = np.abs(X)
print(X.shape)

# %% [markdown]
# ## Define model

# %%
POOLS = 3
inputs = keras.Input((256, 1024, 1))

# Encoder - Conv2D gradually down to LSTM
# Conv1D didn't work as expected - instead, using conv2d but width of sliding window is 1

filter_expand = inputs
for i in range(POOLS):
    batch_norm = layers.BatchNormalization()(filter_expand)
    conv = layers.Conv2D(2**i, (1, 3), (1, 1), padding='same', activation='relu')(batch_norm)
    # add
    pool = layers.MaxPool2D((1, 2), (1, 2))(conv)   # (add)
    filter_expand = layers.Conv2D(2**(i+1), (1, 3), (1, 1), padding='same', activation='relu')(pool)

lstm_input = tf.reshape(filter_expand, (-1, 256, 1024))

lstm = layers.LSTM(128, return_sequences=True)(lstm_input)
dense = layers.Dense(2**10, activation='sigmoid')(lstm)
dense_reshaped = tf.reshape(dense, (-1, 256, 1024//2**POOLS, 2**POOLS))

conv = dense_reshaped
for i in range(POOLS):
    batch_norm = layers.BatchNormalization()(conv)
    filter_reduce = layers.Conv2D(2**(POOLS - i - 1), (1, 3), (1,1), padding='same', activation='relu')(batch_norm)
    depool = layers.UpSampling2D((1, 2))(filter_reduce)
    conv = layers.Conv2D(2**(POOLS - i - 1), (1, 3), (1, 1), padding='same', activation='relu')(depool)

outputs = layers.Activation('sigmoid')(conv)
model = keras.Model(inputs=inputs, outputs=outputs, name="conv1d-lstm")

for layer in model.layers[-10:]:
    print(layer.output_shape)

# %%
model.compile(optimizer='adam', loss='binary_crossentropy')
model.summary()

# %%
X_fit = np.expand_dims(X, -1)
X_fit = (X_fit - np.min(X_fit))/(np.max(X_fit) - np.min(X_fit))

print("==================")
print(X_fit.shape)
print("==================")


# %%
# model.load_weights("lstm_autoencoder")

# %%
model.fit(X_fit, X_fit,
        epochs=200,
        shuffle=True
)

# %%
model.save("lstm_autoencoder")

# %% [markdown]
# ### COMPARE SPECTROGRAMS IN IMAGES
# 

# %%
import matplotlib.pyplot as plt

# %%
x_example = X[0]

plt.imsave("INPUT_EXAMPLE.png", x_example)
x_example = np.reshape(x_example, (1, x_example.shape[0], x_example.shape[1], 1))
print(x_example.shape)
prediction = model.predict(x_example)
plt.imsave("OUTPUT_EXAMPLE.png", prediction[0, :, :, 0])

# %% [markdown]
# ### Save to audio file

# %%
import importlib
import postprocessing

# %%
importlib.reload(postprocessing)
out_samp, out_win, out_stride = spec_params
audio = postprocessing.reverse_spectrogram(prediction[0, :, :, 0], out_samp, out_win, out_stride)
audio = np.reshape(audio, (-1, 1))
f_out = open_write("test_output_cnn.wav", 1, 2, 44100)
write(f_out, audio)

# %%



