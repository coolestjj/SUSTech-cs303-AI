import sys
import numpy as np
import argparse


if __name__ == '__main__':
    filename = sys.argv[1]
    print(filename)
    file = open(filename)
    line = file.readlines()

    vertices_num = int(line[1].split(':')[1].replace('\n', ''))
    depot = int(line[2].split(':')[1].replace('\n', ''))
    required_edges = int(line[3].split(':')[1].replace('\n', ''))
    non_required_edges = int(line[4].split(':')[1].replace('\n', ''))
    cars_num = int(line[5].split(':')[1].replace('\n', ''))
    capacity = int(line[6].split(':')[1].replace('\n', ''))
    total_cost = int(line[7].split(':')[1].replace('\n', ''))

    cost_graph = np.zeros((vertices_num + 1, vertices_num + 1))
    demand_graph = np.ones((vertices_num + 1, vertices_num + 1))
    demand_graph = demand_graph * (-1)

    i = 9
    while line[i] != 'END':
        element = line[i].split(' ')
        node1 = int(element[0])
        node2 = int(element[1])
        cost = int(element[2])
        demand = int(element[3])
        cost_graph[node1][node2] = cost
        cost_graph[node2][node1] = cost
        demand_graph[node1][node2] = demand
        demand_graph[node2][node1] = demand
        i += 1

    parse = argparse.ArgumentParser()
    parse.add_argument('-t')
    parse.add_argument('-s')
    a = parse.parse_args()
    dic = vars(a)
    termination_time = int(dic['t'])
    random_seed = int(dic['s'])

    print(vertices_num)
    print(capacity)
    print(termination_time)
    print(random_seed)
