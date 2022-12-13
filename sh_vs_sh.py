import random
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
        self.is_red = 0

    def random_color(self):
        global red_num, blue_num
        for child in self.children:
            node_array[child].random_color()
        if self.parent != -1:
            if red_num != 0 and blue_num != 0:
                self.is_red = random.randrange(0, 2)
                if self.is_red:
                    red_num -= 1
                else:
                    blue_num -= 1
            elif red_num == 0:
                self.is_red = 0
                blue_num -= 1
            else:
                self.is_red = 1
                red_num -= 1
            node_array[self.parent].red_sub_nodes += self.red_sub_nodes
            node_array[self.parent].blue_sub_nodes += self.blue_sub_nodes
            if self.is_red:
                node_array[self.parent].red_sub_nodes += 1
            else:
                node_array[self.parent].blue_sub_nodes += 1





    def dfs(self):
        for child in self.children:
            node_array[child].parent = self.idx
            node_array[child].dfs()
        if self.parent != -1:
            node_array[self.parent].sub_nodes += self.sub_nodes


input = sys.argv[1]
fp = open(input, 'r')
node_num = int(fp.readline())
node_array = np.empty(node_num + 1, dtype=Node)
for i, line in enumerate(fp):
    node_array[i + 1] = Node(i + 1)
    node_array[i + 1].children = np.delete([int(i) for i in line.split()], 0)
    node_array[i + 1].degree = len(node_array[i + 1].children)

saved_blue_num = 0
saved_red_num = 0
saved_num = 0
node_array[1].dfs()

blue_num = node_num // 2
red_num = blue_num
node_array[1].random_color()
print("blue", blue_num)
print("red", red_num)

bfs_queue = [1]
while bfs_queue:
    select = - 1
    max_sub_nodes = 0
    last_level_len = len(bfs_queue)
    for i in range(last_level_len):
        for child in node_array[bfs_queue[i]].children:
            if node_array[child].blue_sub_nodes + node_array[child].red_sub_nodes >= max_sub_nodes:
                max_sub_nodes = node_array[child].red_sub_nodes + node_array[child].blue_sub_nodes
                select = len(bfs_queue)
            bfs_queue.append(child)

    if select != -1:
        print("select", bfs_queue[select])
        saved_num += node_array[bfs_queue[select]].red_sub_nodes + node_array[bfs_queue[select]].blue_sub_nodes + 1
        saved_red_num += node_array[bfs_queue[select]].red_sub_nodes
        saved_blue_num += node_array[bfs_queue[select]].blue_sub_nodes
        if node_array[bfs_queue[select]].is_red:
            saved_red_num += 1
        else:
            saved_blue_num += 1
        bfs_queue.pop(select)
    for i in range(last_level_len):
        bfs_queue.pop(0)
#         1
#     2       3
# 4 5 6 7   8    9
#         10 11   12

print("blue save", saved_blue_num)
print("red save", saved_red_num)
print("save", saved_num)
print(f'{saved_blue_num}/{saved_red_num}/{saved_num}')