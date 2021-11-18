import numpy as np
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

speed = 1.5
case_number = 50

while True:
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
    np.set_printoptions(precision=4, suppress=True)
    print(np.sum(all_data, 0))

    save_name = dir_path + '/test_cases.data'
    if os.path.isfile(save_name):
        ans = input("Do you want to overwrite? [Y/n/r] ")
        if 'y' in ans or 'Y' in ans:
            np.savetxt(save_name, all_data)
            print("Saved")
            break
        elif 'r' in ans:
            continue
        else:
            print("Exit withot saving")
            break
