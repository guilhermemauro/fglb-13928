import sys
import os
from loadbalancer import LoadBalancer

if __name__ == '__main__':

    input_file = 'input.txt'
    output_file = 'output.txt'

    if len(sys.argv) > 1:
        if os.path.isfile(sys.argv[1]):
           input_file = sys.argv[1]
        else:
            raise Exception('Input file entered does not exist')

    if len(sys.argv) > 2:
        output_file = sys.argv[2]

    if not os.path.isfile(input_file):
        raise Exception('Default input file does not exists')

    data = []
    print('Loading file in: {}'.format(input_file))
    with open(input_file, 'r') as file:
        for i, val in enumerate(file.read().split('\n')):
            if val.isdigit():
                data.append(int(val))
            else:
                raise Exception('Input values need to be Integers: {} in line {}'.format(val, i))

    lb = LoadBalancer(ttask=data[0], umax=data[1])
    lb.process(tasks=data[2:])
    with open(output_file, 'w+') as file:
        file.write('\n'.join(lb.report))
    print('Done! Written file in {}'.format(output_file))







