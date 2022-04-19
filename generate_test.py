import numpy as np
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
save_name = dir_path + '/test_cases_xyzrpy_25.data'
speed = 1.5
case_number = 25

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
        roll = np.random.normal(0, 20, (case_number, 1))
        if np.abs(np.sum(roll)) < 20:
            break
    while True:
        pitch = np.random.normal(0, 20, (case_number, 1))
        if np.abs(np.sum(pitch)) < 20:
            break
    while True:
        yaw = np.random.normal(0, 180, (case_number, 1))
        if np.abs(np.sum(yaw)) < 180:
            break


    diff_theta = np.reshape(np.diff(np.insert(yaw, 0, 0)), (case_number, 1))
    dis = np.reshape(np.sqrt(xy[:, 0]*xy[:, 0] + xy[:, 1]*xy[:, 1]), (case_number, 1))
    time = dis/speed + np.abs(diff_theta) * 0.05

    all_data = np.concatenate((time, xy, z, roll, pitch, yaw), 1)
    np.set_printoptions(precision=4, suppress=True)
    print(all_data.shape)
    print(np.sum(all_data, 0))

    ans = input("Do you want to save? [Y/n/r] ")
    if 'y' in ans or 'Y' in ans:
        if os.path.exists(save_name):
            ans = input("Override? [Y/n] ")
            if 'n' in ans or 'N' in ans:
                print("Exit withot saving")
                break
        np.savetxt(save_name, all_data)
        print("Saved")
        break
    elif 'r' in ans:
        continue
    else:
        print("Exit withot saving")
        break