from math import sqrt
import random
import time

import numpy as np
from scipy.stats import norm


def random_generator(min_val, max_val, anomaly_rate, deviation=0.1, cap=None):

    normal_range = max_val - min_val
    if random.random() < anomaly_rate:
        offset = normal_range * random.uniform(0.01, deviation)
        if random.choice([True, False]):
            if cap == min_val:
                return max_val + offset
            else:
                return max_val - offset
        else:
            if cap == max_val:
                return min_val - offset
            else:
                return min_val + offset
    else:
        return random.uniform(min_val, max_val)


def brown_generator(init_value, n=500, t=10, delta=2, m=2, data_type="list"):
    dt = t / n  # Time step size

    for _ in range(n):
        output = []
        for idx, init in enumerate(init_value):
            x0 = np.asarray(init)
            r = norm.rvs(size=x0.shape + (1,), scale=delta * sqrt(dt))
            out = np.empty(r.shape)
            np.cumsum(r, axis=-1, out=out)
            out += np.expand_dims(x0, axis=-1)
            output.append(out[0])

        sound = random_generator(30, 50, 0.25, 0.2)
        temp = random_generator(20, 30, 0.15, 0.2)
        altitude = random_generator(1000, 2000, 0.1, 0.2)

        if data_type == "list":
            output = output + [
                sound,
                # 1 if sound_value < 30 or sound_value > 50 else 0,
                temp,
                # 1 if temp < 20 or temp > 30 else 0,
                altitude,
                # 1 if altitude < 1000 or altitude > 2000 else 0,
                time.strftime("%d %B %Y", time.localtime()),
                time.strftime("%H:%M:%S", time.localtime()),
                str(int(time.time() * 1000)),
            ]
        elif data_type == "json":
            output = {
                "latitude": output[0],
                "longitude": output[1],
                "sound": sound,
                "temperature": temp,
                "altitude": altitude,
                "event_ts": int(time.time() * 1000),
                "id": "ids_" + str(int(time.time() * 1000)),
            }

        # print(output)
        # time.sleep(1)
    return output


def brown_generator_location(
    init_value, n=500, t=10, delta=2, m=2, data_type="list"
):
    dt = t / n  # Time step size

    for _ in range(n):
        output = []
        for idx, init in enumerate(init_value):
            x0 = np.asarray(init)
            r = norm.rvs(size=x0.shape + (1,), scale=delta * sqrt(dt))
            out = np.empty(r.shape)
            np.cumsum(r, axis=-1, out=out)
            out += np.expand_dims(x0, axis=-1)
            output.append(out[0])

        if data_type == "list":
            output = output + [
                time.strftime("%d %B %Y", time.localtime()),
                time.strftime("%H:%M:%S", time.localtime()),
                str(int(time.time() * 1000)),
            ]
        elif data_type == "json":
            output = {
                "latitude": output[0],
                "longitude": output[1],
                "event_ts": int(time.time() * 1000),
                "id": "ids_" + str(int(time.time() * 1000)),
            }

        # print(output)
        # time.sleep(1)
    return output


def brown_generator_status(n=500, data_type="list"):

    for _ in range(n):
        sound = random_generator(30, 50, 0.25, 0.2)
        temp = random_generator(20, 30, 0.15, 0.2)
        altitude = random_generator(1000, 2000, 0.1, 0.2)

        if data_type == "list":
            output = [
                sound,
                # 1 if sound_value < 30 or sound_value > 50 else 0,
                temp,
                # 1 if temp < 20 or temp > 30 else 0,
                altitude,
                # 1 if altitude < 1000 or altitude > 2000 else 0,
                time.strftime("%d %B %Y", time.localtime()),
                time.strftime("%H:%M:%S", time.localtime()),
                str(int(time.time() * 1000)),
            ]
        elif data_type == "json":
            output = {
                "sound": sound,
                "temperature": temp,
                "altitude": altitude,
                "event_ts": int(time.time() * 1000),
                "id": "ids_" + str(int(time.time() * 1000)),
            }

        # print(output)
        # time.sleep(1)
    return output
