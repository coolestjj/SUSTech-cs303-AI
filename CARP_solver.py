import sys
import numpy as np


# def dijkstra(cost_graph):
#     dis = np.zeros((len(cost_graph), len(cost_graph)))
#     for start in range(1, len(cost_graph)):
#         visited = [0] * (len(cost_graph))
#         visited[start] = 1
#         distance = [9999999] * (len(cost_graph))
#         for i in range(1, len(cost_graph)):
#             distance[i] = cost_graph[start][i]
#         for i in range(1, len(cost_graph)):
#             MIN = 9999999
#             unvisited = 0
#             for j in range(1, len(cost_graph)):
#                 if visited[j] == 0 and distance[j] < MIN:
#                     MIN = distance[j]
#                     unvisited = j
#             visited[unvisited] = 1
#             for j in range(1, len(cost_graph)):
#                 if cost_graph[unvisited][j] != 9999999:
#                     distance[j] = min(distance[j], distance[unvisited] + cost_graph[unvisited][j])
#         for i in range(1, len(cost_graph)):
#             dis[start][i] = distance[i]
#     return dis


def floyd(cost_graph):
    dis = np.copy(cost_graph)
    for k in range(1, len(cost_graph)):
        for i in range(1, len(cost_graph)):
            for j in range(1, len(cost_graph)):
                if dis[i][j] > dis[i][k] + dis[k][j]:
                    dis[i][j] = dis[i][k] + dis[k][j]
    return dis


def path_scanning(depot, cost_graph, demand_graph, free, capacity, dis):
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
                    elif dis[start][arc[0]] == dis2 and dis[arc[1]][start] < dis[arc2[1]][start]:
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
        # result.append(route)

    return result, q


if __name__ == '__main__':
    filename = sys.argv[1]
    file = open(filename)
    line = file.readlines()

    vertices_num = int(line[1].split(':')[1].replace('\n', ''))
    depot = int(line[2].split(':')[1].replace('\n', ''))
    required_edges = int(line[3].split(':')[1].replace('\n', ''))
    non_required_edges = int(line[4].split(':')[1].replace('\n', ''))
    cars_num = int(line[5].split(':')[1].replace('\n', ''))
    capacity = int(line[6].split(':')[1].replace('\n', ''))
    total_cost = int(line[7].split(':')[1].replace('\n', ''))
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

    # dis = dijkstra(cost_graph)
    dis = floyd(cost_graph)
    # Python CARP_solver.py egl-e1-A.dat -t 123 -s 124

    free = []
    for i in range(1, vertices_num + 1):
        for j in range(1, vertices_num + 1):
            if demand_graph[i][j] != 0 and (i, j) not in free and (j, i) not in free:
                free.append((i, j))
                free.append((j, i))

    result, q = path_scanning(depot, cost_graph, demand_graph, free, capacity, dis)
    modified_result = str(result).replace(" ", "").replace("[[", "s 0,").replace("]]", ",0").replace("]", ",0").replace(
        "[", "0,")

    print(modified_result)
    print("q", int(q))
    # print(cost_graph)
    # print()
    # print(dijkstra(cost_graph))
    # print()
    # print(floyd(cost_graph))
