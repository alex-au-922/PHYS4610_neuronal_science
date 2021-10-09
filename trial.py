from utils.parser import parse_arg
import yaml

args = parse_arg()
with open('constants.yaml') as stream:
    buff_arg = yaml.safe_load(stream)
for key, value in buff_arg.items():
    if 'dt' in value:
        value['dt'] = args.dt
    if 'totalTime' in value:
        value['totalTime'] = args.totalTime
    if 'maxSpike' in value:
        value['maxSpike'] = args.maxSpike

print(buff_arg['Main'].dt)
