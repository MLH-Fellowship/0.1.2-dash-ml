import keras
from keras.datasets import mnist
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Dense, Dropout, Flatten
from keras.models import Sequential


def generate_model():
    (X_train, y_train), (X_test, y_test) = mnist.load_data()

    X_train = X_train.reshape(60000, 28, 28, 1)
    X_test = X_test.reshape(10000, 28, 28, 1)

    X_train = X_train.astype('float32')
    X_test = X_test.astype('float32')
    X_train /= 255
    X_test /= 255

    y_train = keras.utils.to_categorical(y_train, 10)
    y_test = keras.utils.to_categorical(y_test, 10)

    model = Sequential()
    model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(28, 28, 1)))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(10, activation='softmax'))

    model.compile(loss=keras.losses.categorical_crossentropy,
                  optimizer=keras.optimizers.Adadelta(),
                  metrics=['accuracy'])

    model.summary()
    model.fit(X_train, y_train, batch_size=128, verbose=0, epochs=5, validation_data=(X_test, y_test))
    return model


if __name__ == '__main__':
    mnist_model = None
    try:
        mnist_model = keras.models.load_model("mnist_model")
        print("Using pre-existing model at mnist_model")
    except OSError:
        print("Could not find a pre-existing model at mnist_model, generating a new one")
        mnist_model = generate_model()
        mnist_model.save("mnist_model")
        print("New model generated stored at mnist_model")
    _, (x_test, y_test) = mnist.load_data()
    (loss, accuracy) = mnist_model.evaluate(x_test.reshape(10000, 28, 28, 1), keras.utils.to_categorical(y_test, 10),
                                            verbose=0)
    print("The model's accuracy is {:4.2f}".format(accuracy * 100))

