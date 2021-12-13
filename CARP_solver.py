import sys
import numpy as np
import time


def floyd(cost_graph):
    dis = np.copy(cost_graph)
    for k in range(1, len(cost_graph)):
        for i in range(1, len(cost_graph)):
            for j in range(1, len(cost_graph)):
                if dis[i][j] > dis[i][k] + dis[k][j]:
                    dis[i][j] = dis[i][k] + dis[k][j]
    return dis


def path_scanning(depot, cost_graph, demand_graph, vertices_num, capacity, dis, mode):
    free = make_free(demand_graph, vertices_num)
    result = []
    q = 0
    while True:
        route = []
        cap = capacity
        start = depot

        while True:
            dis2 = 9999999
            for arc in free:
                if demand_graph[arc[0]][arc[1]] < cap:
                    if dis[start][arc[0]] < dis2:
                        dis2 = dis[start][arc[0]]
                        arc2 = arc
                    elif dis[start][arc[0]] == dis2:
                        if mode == 1:
                            if dis[arc[1]][start] < dis[arc2[1]][start]:
                                arc2 = arc
                        if mode == 2:
                            if dis[arc[1]][start] > dis[arc2[1]][start]:
                                arc2 = arc
                        if mode == 3:
                            if demand_graph[arc[0]][arc[1]] / cost_graph[arc[0]][arc[1]] < demand_graph[arc2[0]][arc2[1]] / cost_graph[arc2[0]][arc2[1]]:
                                arc2 = arc
                        if mode == 4:
                            if demand_graph[arc[0]][arc[1]] / cost_graph[arc[0]][arc[1]] > demand_graph[arc2[0]][arc2[1]] / cost_graph[arc2[0]][arc2[1]]:
                                arc2 = arc
                        if mode == 5:
                            if cap < capacity / 2:
                                if dis[arc[1]][start] < dis[arc2[1]][start]:
                                    arc2 = arc
                            elif cap >= capacity / 2:
                                if dis[arc[1]][start] > dis[arc2[1]][start]:
                                    arc2 = arc

            if free == [] or dis2 == 9999999:
                break
            route.append(arc2)
            q += cost_graph[arc2[0]][arc2[1]] + dis[start][arc2[0]]
            free.remove(arc2)
            free.remove((arc2[1], arc2[0]))
            start = arc2[1]
            cap = cap - demand_graph[arc2[0]][arc2[1]]

        result.append(route)
        q += dis[start][depot]
        if not free:
            break

    return result, q


def make_free(demand_graph, vertices_num):
    free = []
    for i in range(1, vertices_num + 1):
        for j in range(1, vertices_num + 1):
            if demand_graph[i][j] != 0 and (i, j) not in free and (j, i) not in free:
                free.append((i, j))
                free.append((j, i))
    return free


if __name__ == '__main__':

    start = time.time()

    filename = sys.argv[1]
    file = open(filename)
    line = file.readlines()

    vertices_num = int(line[1].split(':')[1].replace('\n', ''))
    depot = int(line[2].split(':')[1].replace('\n', ''))
    capacity = int(line[6].split(':')[1].replace('\n', ''))
    termination_time = sys.argv[3]
    random_seed = sys.argv[5]

    cost_graph = np.ones((vertices_num + 1, vertices_num + 1))
    cost_graph = cost_graph * 9999999
    for i in range(1, vertices_num + 1):
        cost_graph[i][i] = 0

    demand_graph = np.zeros((vertices_num + 1, vertices_num + 1))

    dis = np.zeros((vertices_num + 1, vertices_num + 1))

    i = 9
    while line[i] != 'END':
        element = line[i].split()
        node1 = int(element[0])
        node2 = int(element[1])
        cost = int(element[2])
        demand = int(element[3])
        cost_graph[node1][node2] = cost
        cost_graph[node2][node1] = cost
        demand_graph[node1][node2] = demand
        demand_graph[node2][node1] = demand
        i += 1

    dis = floyd(cost_graph)
    # Python CARP_solver.py egl-e1-A.dat -t 123 -s 124
    # Python CARP_solver.py egl-s1-A.dat -t 123 -s 124
    # Python CARP_solver.py gdb1.dat -t 123 -s 124
    # Python CARP_solver.py gdb10.dat -t 123 -s 124
    # Python CARP_solver.py val1A.dat -t 123 -s 124
    # Python CARP_solver.py val4A.dat -t 123 -s 124
    # Python CARP_solver.py val7A.dat -t 123 -s 124

    result1, q1 = path_scanning(depot, cost_graph, demand_graph, vertices_num, capacity, dis, 1)
    result2, q2 = path_scanning(depot, cost_graph, demand_graph, vertices_num, capacity, dis, 2)
    result3, q3 = path_scanning(depot, cost_graph, demand_graph, vertices_num, capacity, dis, 3)
    result4, q4 = path_scanning(depot, cost_graph, demand_graph, vertices_num, capacity, dis, 4)
    result5, q5 = path_scanning(depot, cost_graph, demand_graph, vertices_num, capacity, dis, 5)

    q = min(q1, q2, q3, q4, q5)
    result = []
    if q == q1:
        result = result1
        # print(1)
    elif q == q2:
        result = result2
        # print(2)
    elif q == q3:
        result = result3
        # print(3)
    elif q == q4:
        result = result4
        # print(4)
    elif q == q5:
        result = result5

    modified_result = str(result).replace(" ", "").replace("[[", "s 0,").replace("]]", ",0").replace("]", ",0").replace(
        "[", "0,")

    run_time = time.time() - start

    print(modified_result)
    print("q", int(q))
    # print(run_time)

