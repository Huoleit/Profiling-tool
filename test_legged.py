from subprocess import check_output, Popen, DEVNULL, PIPE, CalledProcessError
import time
from numpy import loadtxt
import os
from datetime import datetime
from pathlib import Path
import toml

def checkExists(path):
    if not Path(path).exists():
        raise RuntimeError("Can NOT find file " + path) 

def limitInput(x, control, limit):
    if abs(x) > abs(limit):
        if abs(x - limit) < abs(x + limit):
            return [control - x + limit, limit]
        else:
            return [control - x - limit, -limit]
    else:
        return [control, x]
    

dir_path = os.path.dirname(os.path.realpath(__file__))
configFile = dir_path + "/config.toml"
checkExists(configFile)

settings = toml.load(configFile)
# print(settings)
print("=================================")
print(toml.dumps(settings))
print("=================================")

test_file = dir_path + '/' + settings['test_file']
checkExists(test_file)

# Load and scale test cases
test_cases = loadtxt(test_file)
time_scale = settings['time_scale']
all_time = sum([c[0] * time_scale for c in test_cases])

checkExists(settings['launch']['gait_config_path'])
checkExists(settings['launch']['target_config_path'])
checkExists(settings['launch']['launch_file_path'])

try:
    check_output(['rospack', 'find', settings['launch']['package_name']])
except CalledProcessError:
    print("Please source the workspace setup file.")
    exit()

try:
    Path(dir_path + settings['log']['root_dir']).mkdir(exist_ok=True)
    f = open(dir_path + settings['log']['root_dir'] + '/' + settings['log']['log_prefix'] + '-' + str(datetime.now()) + '.txt', 'w')
    p_launch = Popen(['roslaunch', settings['launch']['launch_file_path']], stderr=f, stdin=DEVNULL, stdout=DEVNULL, encoding='UTF-8', bufsize=0)
    time.sleep(settings['wait_before_start_trot_s'])
    p_gait = Popen(['rosrun', settings['launch']['package_name'], settings['launch']['gait_command_node_name']] + settings['launch']['gait_command_node_args'], stderr=DEVNULL, stdin=PIPE, stdout=DEVNULL, encoding='UTF-8', bufsize=0)
    p_target = Popen(['rosrun', settings['launch']['package_name'], settings['launch']['target_command_node_name']] + settings['launch']['target_command_node_args'], stderr=DEVNULL, stdin=PIPE, stdout=DEVNULL, encoding='UTF-8', bufsize=0)
    print("Trot")
    p_gait.stdin.flush()
    p_gait.stdin.write('trot\n')
    p_gait.stdin.flush()
    time.sleep(2)

    in_stream = p_target.stdin
    in_stream.flush()
    start_time = time.time()
    x = 0
    y = 0
    for c in test_cases:
        # x = x+c[1]
        # y = y+c[2]
        # limit = 1
        # c[1], x = limitInput(x, c[1], limit)
        # c[2], y = limitInput(y, c[2], limit)

        in_stream.write(' '.join(map(str, c[1:])) + '\n')
        time.sleep(c[0] * time_scale)
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
