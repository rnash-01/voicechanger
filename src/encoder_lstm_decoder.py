import tensorflow as tf
from tensorflow import keras
from dataset import *

def residual_block(inputs, num_filters, block_name='ResBlock'):
    with K.name_scope(block_name):
        conv1d_1 = keras.layers.Conv1D(num_filters, kernel_size=10, padding='same')(inputs)
        batch_norm_1 = keras.layers.BatchNormalization()(conv1d_1)
        activation_1 = keras.layers.Activation('relu')(batch_norm_1)
        conv1d_2 = keras.layers.Conv1D(num_filters, kernel_size=10, padding='same')(activation_1)
        batch_norm_2 = keras.layers.BatchNormalization()(conv1d_2)
        activation_2 = keras.layers.Activation('relu')(batch_norm_2 + inputs)
    return activation_2

def upscale_block(inputs, target_size, num_filters, block_name='UpscaleBlock'):
    with K.name_scope(block_name):
        in_shape = tf.shape(inputs)
        upscale = keras.layers.Conv1DTranspose(num_filters, target_size - in_shape + 1)(inputs)
        batch_norm = keras.layers.BatchNormalization()(upscale)
        activation = keras.layers.Activation('relu')(batch_norm)

    return activation


def encoder_lstm_decoder(win_size, samp_rate, encoding_dim, start_filters):
    input_length = (win_size * samp_rate)//2 + 1                                # DOUBLE CHECK THIS

    # Encoder
    inputs = keras.layers.Input((input_length,))                                # input_length is power of two

    res_block_1 = residual_block(inputs, start_filters, 'ResBlock1')
    max_pool_1 = keras.layers.MaxPool1D(pool_size=2)(res_block_1)               # (input_length/2,)

    res_block_2 = residual_block(max_pool_1, start_filters * 2, 'ResBlock2')
    max_pool_2 = keras.layers.MaxPool1D(pool_size=2)(res_block_2)               # (input_length/4,)

    res_block_3 = residual_block(max_pool_2, start_filters * 4, 'ResBlock3')
    max_pool_3 = keras.layers.MaxPool1D(pool_size=2)(res_block_3)               # (input_length/8,)

    res_block_4= residual_block(max_pool_3, start_filters * 8, 'ResBlock3')
    max_pool_4 = keras.layers.MaxPool1D(pool_size=2)(res_block_4)               # (input_length/16,)

    # Decoder
    lstm = keras.layers.LSTM(encoding_dim, return_sequences=True)(max_pool_4)

    upscale_1 = upscale_block(lstm, input_length/8, start_filters * 8, 'Upscale1')
    upscale_2 = upscale_block(upscale_1, input_length/4, start_filters * 4, 'Upscale2')
    upscale_3 = upscale_block(upscale_2, input_length/2, start_filters * 2, 'Upscale3')
    upscale_4 = upscale_block(upscale_3, input_length, start_filters, 'Upscale4')
    
    outputs = keras.layers.Dense(input_length, activation='sigmoid')(upscale_4)
    
    model = keras.Model(inputs=inputs, outputs=outputs)
    return model

