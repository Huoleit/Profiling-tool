from subprocess import check_output, Popen, DEVNULL, PIPE
import time
from numpy import loadtxt
import os
from datetime import datetime
from pathlib import Path


dir_path = os.path.dirname(os.path.realpath(__file__))
test_cases = loadtxt(dir_path + '/test_cases.data')

all_time = sum([c[0] for c in test_cases])
ocs2_legged_robot_dir = check_output(['rospack', 'find', 'ocs2_legged_robot'], encoding='UTF-8')[:-1]
gait_config_path = ocs2_legged_robot_dir + '/config/command/gait.info'
target_command_config_path = ocs2_legged_robot_dir + '/config/command/targetTrajectories.info'
launch_file = ocs2_legged_robot_dir + '/launch/legged_robot.launch'
print("Find ocs2 in " + ocs2_legged_robot_dir)
print("Launch file " + launch_file)

try:
    Path(dir_path + "/log").mkdir(exist_ok=True)
    f = open(dir_path + '/log/launch_result-' + str(datetime.now()), 'w')
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
    for c in test_cases:
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
