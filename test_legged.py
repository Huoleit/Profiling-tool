from subprocess import check_output, Popen, DEVNULL, PIPE
import time

tests = [[2.37434123e+00, -1.99022012e+00,  1.56742557e+00,
          6.50180872e-02, -6.85449542e+01],
         [1.95804154e+00, -3.96207197e-01, -9.60593471e-01,
          1.91159165e-02, -1.95076059e+02],
         [4.38515923e+00, -2.75838907e+00, -1.38634842e+00,
          2.32175626e-03,  3.76279523e+01],
         [7.72033258e+00,  4.68191567e+00,  3.14244606e+00,
          2.33909118e-02, -3.58489821e+02],
         [5.12636914e+00,  2.34489879e+00,  5.12073132e-01,
          -5.27912336e-02, -5.86359088e+00],
         [1.50390350e+00,  1.07180649e+00, -1.74594273e+00,
          -1.10411593e-02,  7.94816650e+00],
         [5.53850028e-01,  4.27590647e-01, -4.18307488e-01,
          -2.42478109e-02, -7.55841467e+00],
         [2.12141320e+00, -1.21007313e+00, -2.21633746e+00,
          -1.32150875e-01,  3.62389618e+01],
         [3.25746525e+00, -3.62734340e+00, -2.88571632e-01,
          -4.22486435e-02, -4.69206375e+01],
         [7.26741197e+00, -2.33834416e+00,  5.71126835e+00,
          -2.91673578e-02,  2.68392480e+02],
         [4.48322760e+00,  1.41487388e+00, -1.72759798e+00,
          4.69642502e-02, -3.10610175e+01],
         [4.67086946e+00,  1.76033635e+00, -1.96566492e+00,
          1.09372077e-01, -3.22236084e+02],
         [4.13949813e+00,  5.74850394e-01, -4.08366891e-01,
          -1.57277365e-03,  4.47046760e+01],
         [1.63232530e+00, -1.51325070e+00, -1.24210309e+00,
          -4.26584907e-02,  7.74211736e+01],
         [2.53119826e+00, -1.36637799e+00, -1.21586834e-01,
          -6.69657535e-02,  2.39089199e+02],
         [5.33768514e+00,  1.50025123e-01,  2.57404378e+00,
          2.56430645e-02, -1.22785175e+02],
         [1.60183996e+00,  1.32430741e+00,  7.18870339e-01,
          -9.26128471e-02, -1.82513218e+02],
         [4.06302611e+00, -4.05334094e-01, -4.15375223e-01,
          -5.52824965e-03,  1.85097889e+02],
         [3.52890557e+00,  1.25876486e-01,  2.97865447e+00,
          5.45455162e-02,  3.09615330e+01],
         [3.07188956e+00,  2.47178986e+00, -2.48780047e+00,
          -5.07038268e-02, -4.24288749e+01],
         [2.90946849e+00,  2.95490142e-01, -4.61052439e-01,
          3.28130172e-02,  2.12010211e+02],
         [2.15086289e+00,  1.38573373e+00,  1.20681798e+00,
          -4.72497911e-02,  1.19428663e+02],
         [2.96311340e+00,  1.53652970e+00, -1.08775201e+00,
          9.16345808e-02, -5.13769811e+01],
         [3.02222620e+00, -1.05924171e+00,  2.48290984e+00,
          -1.27872089e-02,  7.08847265e+01],
         [2.19547426e+00, -1.35962129e+00, -2.37937253e+00,
          2.29472075e-02,  1.07736489e+02]]

all_time = sum([c[0] for c in tests])
ocs2_legged_robot_dir = check_output(['rospack', 'find', 'ocs2_legged_robot'], encoding='UTF-8')[:-1]
gait_config_path = ocs2_legged_robot_dir + '/config/command/gait.info'
target_command_config_path = ocs2_legged_robot_dir + '/config/command/targetTrajectories.info'
launch_file = ocs2_legged_robot_dir + '/launch/legged_robot.launch'
print("Find ocs2 in " + ocs2_legged_robot_dir)
print("Launch file " + launch_file)

try:
    f = open('launch_result', 'w')
    p_launch = Popen(['roslaunch', launch_file], stderr=f, stdin=DEVNULL, stdout=DEVNULL, encoding='UTF-8', bufsize=0)
    time.sleep(15)
    p_gait = Popen(['rosrun', 'ocs2_legged_robot', 'legged_robot_gait_command', 'legged_robot',
                    gait_config_path], stderr=DEVNULL, stdin=PIPE, stdout=DEVNULL, encoding='UTF-8', bufsize=0)
    p_target = Popen(['rosrun', 'ocs2_legged_robot', 'legged_robot_target', 'legged_robot',
                      target_command_config_path], stderr=DEVNULL, stdin=PIPE, stdout=DEVNULL, encoding='UTF-8', bufsize=0)
    print("Trot")
    p_gait.stdin.flush()
    p_gait.stdin.write('trot\n')
    p_gait.stdin.flush()
    time.sleep(2)

    in_stream = p_target.stdin
    in_stream.flush()
    start_time = time.time()
    for c in tests:
        in_stream.write(' '.join(map(str, c[1:])) + '\n')
        time.sleep(c[0])
        time_elapsed = time.time() - start_time
        print('\rTime: ' + str(time_elapsed) + ' ' + str(round(time_elapsed/all_time * 100, 1)) + '%', end='')

except Exception as e:
    raise(e)

finally:
    try:
        f.close()
    except:
        pass

    try:
        p_target.terminate()
    except:
        pass

    try:
        p_gait.terminate()
    except:
        pass

    try:
        p_launch.terminate()
    except:
        pass
