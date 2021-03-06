import datetime
import socket
import pickle

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.optimizers import Adam

from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import SGDRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

from keras.wrappers.scikit_learn import KerasRegressor

from modules.sampling.data_util import build_dataset


def runKNN(inputs, ks):

    if inputs:
        data = pickle.loads(inputs)
    else:
        data = build_dataset()

    outputs = []

    ts = datetime.datetime.now()

    for k in ks:
        model = KNeighborsRegressor(n_neighbors=k)
        model.fit(data["x_train"], data["y_train"])

        score = model.score(data["x_val"], data["y_val"])
        preds = model.predict(data["x_test"])

        pred = preds.reshape(len(preds))
        real = data["y_test"]

        # Compute the mean squared error of our predictions.
        mse = mean_squared_error(real, pred)

        output = {}
        output['cross_val_score'] = score
        output['mse'] = mse
        output['k'] = k

        outputs.append(output)

    ts = datetime.datetime.now() - ts
    h = socket.gethostname()

    return {
        "msg": "Run KNN! [" + h + "] > elapsed time: " + str(ts),
        "data": outputs,
    }


def runLinearRegretion(inputs, lrs):
    if inputs:
        data = pickle.loads(inputs)
    else:
        data = build_dataset()

    outputs = []

    ts = datetime.datetime.now()

    for lr in lrs:
        model = SGDRegressor(
            eta0=lr,
            max_iter=700,
            random_state=42
        )
        model.fit(data["x_train"], data["y_train"])

        preds = model.predict(data["x_test"])
        score = model.score(data["x_val"], data["y_val"])

        pred = preds.reshape(len(preds))
        real = data["y_test"]

        mse = mean_squared_error(real, pred)

        output = {}
        output['score'] = score
        output['mse'] = mse
        output['lr'] = lr

        outputs.append(output)

    ts = datetime.datetime.now() - ts
    h = socket.gethostname()

    return {
        "msg": "Run LReg! [" + h + "] > elapsed time: " + str(ts),
        "data": outputs,
    }


def runRForest(inputs, hp):
    if inputs:
        data = pickle.loads(inputs)
    else:
        data = build_dataset()

    ts = datetime.datetime.now()

    outputs = []
    for n_estimator, max_depth in hp:
        model = RandomForestRegressor(
            n_estimators=n_estimator,
            max_depth=max_depth,
            random_state=42,
            verbose=1,
            n_jobs=1
        )

        model.fit(data["x_train"], data["y_train"])

        score = model.score(data["x_val"], data["y_val"])
        preds = model.predict(data["x_test"])

        pred = preds.reshape(len(preds))
        real = data["y_test"]

        mse = mean_squared_error(real, pred)

        output = {}
        output['score'] = score
        output['mse'] = mse
        output['hp'] = [n_estimator, max_depth]

        outputs.append(output)

    ts = datetime.datetime.now() - ts
    h = socket.gethostname()

    return {
        "msg": "Run LReg! [" + h + "] > elapsed time: " + str(ts),
        "data": outputs,
    }


def runANN(inputs, hp):
    if inputs:
        data = pickle.loads(inputs)
    else:
        data = build_dataset()

    ts = datetime.datetime.now()


    outputs = []
    for l1_units, l2_units in hp:
        model = KerasRegressor(build_fn=create_baseline_model, l1_units=l1_units, l2_units=l2_units, verbose=0)

        model.fit(
            data["x_train"],
            data["y_train"],
            verbose=0,
            validation_data=(data["x_val"], data["y_val"]),
            epochs=300
        )

        score = model.score(data["x_val"], data["y_val"])
        preds = model.predict(data["x_test"])

        pred = preds.reshape(len(preds))
        real = data["y_test"]

        mse = mean_squared_error(real, pred)

        output = {}
        output['score'] = score
        output['mse'] = mse
        output['hp'] = [l1_units, l2_units]

        outputs.append(output)


    ts = datetime.datetime.now() - ts
    h = socket.gethostname()


    return {
        "msg": "Run ANN! [" + h + "] > elapsed time: " + str(ts),
        "data": outputs,
    }


def create_baseline_model(l1_units=300, l1_dp=0.1, l2_units=150, l2_dp=0.05, lr=0.001):
    model = Sequential()
    model.add(Dense(l1_units, input_dim=5, kernel_initializer='normal', activation='relu'))
    model.add(Dropout(l1_dp))
    model.add(Dense(l2_units, kernel_initializer='normal', activation='relu'))
    model.add(Dropout(l2_dp))
    model.add(Dense(1, kernel_initializer='normal', activation='linear'))

    adam = Adam(lr=lr)
    model.compile(loss='mse', optimizer=adam, metrics=['mse'])

    return model