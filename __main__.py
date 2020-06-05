import asyncio

import keras
import websockets
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

    # https://keras.io/examples/mnist_cnn/
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
    try:
        mnist_model = keras.models.load_model("mnist_model.h5")
        print("Using pre-existing model at mnist_model.h5")
    except OSError:
        print("Could not find a pre-existing model at mnist_model.h5, generating a new one")
        mnist_model = generate_model()
        mnist_model.save("mnist_model.h5")
        print("New model generated stored at mnist_model.h5")
    _, (x_test, y_test) = mnist.load_data()
    (loss, accuracy) = mnist_model.evaluate(x_test.reshape(10000, 28, 28, 1), keras.utils.to_categorical(y_test, 10),
                                            verbose=0)
    print("The model's accuracy is {:4.2f}".format(accuracy * 100))

    dashboards = []




    async def receive_dashboard(websocket, _):
        dashboards.append(websocket)
        (is_are, pluralized_dashboards) = dashboards_pluralize()
        print("A new dashboard has been connected. There {} {} {} connected.".format(is_are, len(dashboards),
                                                                                     pluralized_dashboards))
        while websocket.open:
            pass
        (is_are, pluralized_dashboards) = dashboards_pluralize()
        print("A dashboard disconnected. There {} {} {} connected.".format(is_are, len(dashboards),
                                                                           pluralized_dashboards))


    def dashboards_pluralize():
        return ("is", "dashboard") if len(dashboards) == 1 else ("are", "dashboards")


    start_server = websockets.serve(receive_dashboard, "localhost", 1012)

    asyncio.get_event_loop().run_until_complete(start_server)
    print("A websocket server has been started on port 1012 to serve the dashboard")
    asyncio.get_event_loop().run_forever()
