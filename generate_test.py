import numpy as np


speed = 1.5
case_number = 25

while True:
    xy = np.random.normal(0, 2, (case_number, 2))
    if max(np.abs(np.sum(xy, 0))) < 4:
        break

while True:
    z = np.random.normal(0, 0.05, (case_number, 1))
    if np.abs(np.sum(z)) < 0.2:
        break

while True:
    theta = np.random.normal(0, 180, (case_number, 1))
    if np.abs(np.sum(theta)) < 180:
        break

diff_theta = np.reshape(np.diff(np.insert(theta, 0, 0)), (case_number, 1))
dis = np.reshape(np.sqrt(xy[:, 0]*xy[:, 0] + xy[:, 1]*xy[:, 1]), (case_number, 1))
time = dis/speed + np.abs(diff_theta) * 0.01

all_data = np.concatenate((time, xy, z, theta), 1)
print(repr(all_data))
print(np.sum(all_data, 0))
