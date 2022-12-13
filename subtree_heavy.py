import sys

import numpy as np


class Node:
    def __init__(self, idx):
        self.children = []
        self.idx = idx
        self.parent = -1
        self.blue_sub_nodes = 0
        self.red_sub_nodes = 0
        self.sub_nodes = 0
        self.degree = 0
        self.level = 0
        self.vaccinated = 0

    def dfs(self):
        for child in self.children:
            node_array[child].parent = self.idx
            node_array[child].dfs()
        if self.parent != -1:
            node_array[self.parent].sub_nodes += self.sub_nodes + 1


input = sys.argv[1]
fp = open(input, 'r')
node_num = int(fp.readline())
node_array = np.empty(node_num + 1, dtype=Node)
for i, line in enumerate(fp):
    node_array[i + 1] = Node(i + 1)
    node_array[i + 1].children = np.delete([int(i) for i in line.split()], 0)
    node_array[i + 1].degree = len(node_array[i + 1].children)

saved_num = 0
node_array[1].dfs()
bfs_queue = [1]
while bfs_queue:
    select = - 1
    max_sub_nodes = 0
    max_degree = 0
    last_level_len = len(bfs_queue)
    for i in range(last_level_len):
        for child in node_array[bfs_queue[i]].children:
            if node_array[child].sub_nodes >= max_sub_nodes:
            # if node_array[child].degree >= max_degree:
                max_sub_nodes = node_array[child].sub_nodes
                # max_degree = node_array[child].degree
                select = len(bfs_queue)
            bfs_queue.append(child)

    if select != -1:
        print("select", bfs_queue[select])
        saved_num += node_array[bfs_queue[select]].sub_nodes + 1
        bfs_queue.pop(select)
    for i in range(last_level_len):
        bfs_queue.pop(0)
#         1
#     2       3
# 4 5 6 7   8    9
#         10 11   12

print("save", saved_num)