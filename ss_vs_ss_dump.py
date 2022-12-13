import random
import sys

import numpy as np
import copy
def find_max_red_diff(bfs_queue)-> int:
    select = -1
    max_red_diff = -node_num
    while (bfs_queue):
        last_level_len = len(bfs_queue)
        for i in range(last_level_len):
            for child in node_array[bfs_queue[i]].children:
                if not node_array[child].is_vaccinated and node_array[child].red_sub_nodes - node_array[child].blue_sub_nodes >= max_red_diff:
                    max_red_diff = node_array[child].red_sub_nodes - node_array[child].blue_sub_nodes
                    select = child
                    bfs_queue.append(child)
        for i in range(last_level_len):
            bfs_queue.pop(0)
    return select

def find_max_blue_diff(bfs_queue)-> int:
    select = -1
    max_blue_diff = - node_num
    while (bfs_queue):
        last_level_len = len(bfs_queue)
        for i in range(last_level_len):
            for child in node_array[bfs_queue[i]].children:
                max_diff = node_array[child].red_sub_nodes - node_array[child].blue_sub_nodes
                # print(max_diff)
                if not node_array[child].is_vaccinated and node_array[child].blue_sub_nodes - node_array[child].red_sub_nodes >= max_blue_diff:
                    max_blue_diff = node_array[child].blue_sub_nodes - node_array[child].red_sub_nodes
                    select = child
                    bfs_queue.append(child)
        for i in range(last_level_len):
            bfs_queue.pop(0)
    return select
def update_info(select):
    if select == - 1:
        return

    red = node_array[select].red_sub_nodes
    blue = node_array[select].blue_sub_nodes
    node_array[select].is_vaccinated = 1
    if node_array[select].is_red:
        red += 1
    else:
        blue += 1
    while node_array[select].parent != -1:
        parent = node_array[select].parent
        node_array[parent].red_sub_nodes -= red
        node_array[parent].blue_sub_nodes -= blue
        select = parent

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
        self.is_vaccinated = 0
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
                # print(self.idx, "red")
            else:
                node_array[self.parent].blue_sub_nodes += 1
                # print(self.idx, "blue")





    def dfs(self):
        for child in self.children:
            node_array[child].parent = self.idx
            node_array[child].dfs()
        if self.parent != -1:
            node_array[self.parent].sub_nodes += self.sub_nodes


input = sys.argv[1]
fp = open("testCase1.txt", 'r')
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
start_color = 0 # red = 1, blue = 0
bfs_queue = [1]
round = 0
while bfs_queue:
    last_level_len = len(bfs_queue)
    if round % 2 == start_color:
        bfs_queue_cp = copy.deepcopy(bfs_queue)
        select = find_max_blue_diff(bfs_queue_cp)
        update_info(select)


    else:
        bfs_queue_cp = copy.deepcopy(bfs_queue)
        select = find_max_red_diff(bfs_queue_cp)
        update_info(select)

    for i in range(last_level_len):
        for child in node_array[bfs_queue[i]].children:
            if not node_array[child].is_vaccinated:
                bfs_queue.append(child)

    saved_num += node_array[select].red_sub_nodes + node_array[select].blue_sub_nodes + 1
    saved_red_num += node_array[select].red_sub_nodes
    saved_blue_num += node_array[select].blue_sub_nodes
    if node_array[select].is_red:
        saved_red_num += 1
    else:
        saved_blue_num += 1
    if bfs_queue.count(select) != 0:
        bfs_queue.remove(select)

    for i in range(last_level_len):
        bfs_queue.pop(0)
    round += 1
#         1
#     2       3
# 4 5 6 7   8    9
#         10 11   12
#           1
#     2b 2          3r -1
# 4b 5b 6r 7b   8r 0    9b -1
#           10r 11b       12r


print("blue save", saved_blue_num)
print("red save", saved_red_num)
print("save", saved_num)
print(f'{saved_blue_num}/{saved_red_num}/{saved_num}')

#------------------------------------------------------------------
fp = open("testCase2.txt", 'r')
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
start_color = 0 # red = 1, blue = 0
bfs_queue = [1]
round = 0
while bfs_queue:
    last_level_len = len(bfs_queue)
    if round % 2 == start_color:
        bfs_queue_cp = copy.deepcopy(bfs_queue)
        select = find_max_blue_diff(bfs_queue_cp)
        update_info(select)


    else:
        bfs_queue_cp = copy.deepcopy(bfs_queue)
        select = find_max_red_diff(bfs_queue_cp)
        update_info(select)

    for i in range(last_level_len):
        for child in node_array[bfs_queue[i]].children:
            if not node_array[child].is_vaccinated:
                bfs_queue.append(child)

    saved_num += node_array[select].red_sub_nodes + node_array[select].blue_sub_nodes + 1
    saved_red_num += node_array[select].red_sub_nodes
    saved_blue_num += node_array[select].blue_sub_nodes
    if node_array[select].is_red:
        saved_red_num += 1
    else:
        saved_blue_num += 1
    if bfs_queue.count(select) != 0:
        bfs_queue.remove(select)

    for i in range(last_level_len):
        bfs_queue.pop(0)
    round += 1
#         1
#     2       3
# 4 5 6 7   8    9
#         10 11   12
#           1
#     2b 2          3r -1
# 4b 5b 6r 7b   8r 0    9b -1
#           10r 11b       12r


print("blue save", saved_blue_num)
print("red save", saved_red_num)
print("save", saved_num)
print(f'{saved_blue_num}/{saved_red_num}/{saved_num}')

#------------------------------------------------------------------
fp = open("testCase3.txt", 'r')
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
start_color = 0 # red = 1, blue = 0
bfs_queue = [1]
round = 0
while bfs_queue:
    last_level_len = len(bfs_queue)
    if round % 2 == start_color:
        bfs_queue_cp = copy.deepcopy(bfs_queue)
        select = find_max_blue_diff(bfs_queue_cp)
        update_info(select)


    else:
        bfs_queue_cp = copy.deepcopy(bfs_queue)
        select = find_max_red_diff(bfs_queue_cp)
        update_info(select)

    for i in range(last_level_len):
        for child in node_array[bfs_queue[i]].children:
            if not node_array[child].is_vaccinated:
                bfs_queue.append(child)

    saved_num += node_array[select].red_sub_nodes + node_array[select].blue_sub_nodes + 1
    saved_red_num += node_array[select].red_sub_nodes
    saved_blue_num += node_array[select].blue_sub_nodes
    if node_array[select].is_red:
        saved_red_num += 1
    else:
        saved_blue_num += 1
    if bfs_queue.count(select) != 0:
        bfs_queue.remove(select)

    for i in range(last_level_len):
        bfs_queue.pop(0)
    round += 1
#         1
#     2       3
# 4 5 6 7   8    9
#         10 11   12
#           1
#     2b 2          3r -1
# 4b 5b 6r 7b   8r 0    9b -1
#           10r 11b       12r


print("blue save", saved_blue_num)
print("red save", saved_red_num)
print("save", saved_num)
print(f'{saved_blue_num}/{saved_red_num}/{saved_num}')

#------------------------------------------------------------------
fp = open("testCase4.txt", 'r')
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
start_color = 0 # red = 1, blue = 0
bfs_queue = [1]
round = 0
while bfs_queue:
    last_level_len = len(bfs_queue)
    if round % 2 == start_color:
        bfs_queue_cp = copy.deepcopy(bfs_queue)
        select = find_max_blue_diff(bfs_queue_cp)
        update_info(select)


    else:
        bfs_queue_cp = copy.deepcopy(bfs_queue)
        select = find_max_red_diff(bfs_queue_cp)
        update_info(select)

    for i in range(last_level_len):
        for child in node_array[bfs_queue[i]].children:
            if not node_array[child].is_vaccinated:
                bfs_queue.append(child)

    saved_num += node_array[select].red_sub_nodes + node_array[select].blue_sub_nodes + 1
    saved_red_num += node_array[select].red_sub_nodes
    saved_blue_num += node_array[select].blue_sub_nodes
    if node_array[select].is_red:
        saved_red_num += 1
    else:
        saved_blue_num += 1
    if bfs_queue.count(select) != 0:
        bfs_queue.remove(select)

    for i in range(last_level_len):
        bfs_queue.pop(0)
    round += 1
#         1
#     2       3
# 4 5 6 7   8    9
#         10 11   12
#           1
#     2b 2          3r -1
# 4b 5b 6r 7b   8r 0    9b -1
#           10r 11b       12r


print("blue save", saved_blue_num)
print("red save", saved_red_num)
print("save", saved_num)
print(f'{saved_blue_num}/{saved_red_num}/{saved_num}')
#------------------------------------------------------------------
fp = open("testCase5.txt", 'r')
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
start_color = 0 # red = 1, blue = 0
bfs_queue = [1]
round = 0
while bfs_queue:
    last_level_len = len(bfs_queue)
    if round % 2 == start_color:
        bfs_queue_cp = copy.deepcopy(bfs_queue)
        select = find_max_blue_diff(bfs_queue_cp)
        update_info(select)


    else:
        bfs_queue_cp = copy.deepcopy(bfs_queue)
        select = find_max_red_diff(bfs_queue_cp)
        update_info(select)

    for i in range(last_level_len):
        for child in node_array[bfs_queue[i]].children:
            if not node_array[child].is_vaccinated:
                bfs_queue.append(child)

    saved_num += node_array[select].red_sub_nodes + node_array[select].blue_sub_nodes + 1
    saved_red_num += node_array[select].red_sub_nodes
    saved_blue_num += node_array[select].blue_sub_nodes
    if node_array[select].is_red:
        saved_red_num += 1
    else:
        saved_blue_num += 1
    if bfs_queue.count(select) != 0:
        bfs_queue.remove(select)

    for i in range(last_level_len):
        bfs_queue.pop(0)
    round += 1
#         1
#     2       3
# 4 5 6 7   8    9
#         10 11   12
#           1
#     2b 2          3r -1
# 4b 5b 6r 7b   8r 0    9b -1
#           10r 11b       12r


print("blue save", saved_blue_num)
print("red save", saved_red_num)
print("save", saved_num)
print(f'{saved_blue_num}/{saved_red_num}/{saved_num}')
#------------------------------------------------------------------
fp = open("testCase6.txt", 'r')
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
start_color = 0 # red = 1, blue = 0
bfs_queue = [1]
round = 0
while bfs_queue:
    last_level_len = len(bfs_queue)
    if round % 2 == start_color:
        bfs_queue_cp = copy.deepcopy(bfs_queue)
        select = find_max_blue_diff(bfs_queue_cp)
        update_info(select)


    else:
        bfs_queue_cp = copy.deepcopy(bfs_queue)
        select = find_max_red_diff(bfs_queue_cp)
        update_info(select)

    for i in range(last_level_len):
        for child in node_array[bfs_queue[i]].children:
            if not node_array[child].is_vaccinated:
                bfs_queue.append(child)

    saved_num += node_array[select].red_sub_nodes + node_array[select].blue_sub_nodes + 1
    saved_red_num += node_array[select].red_sub_nodes
    saved_blue_num += node_array[select].blue_sub_nodes
    if node_array[select].is_red:
        saved_red_num += 1
    else:
        saved_blue_num += 1
    if bfs_queue.count(select) != 0:
        bfs_queue.remove(select)

    for i in range(last_level_len):
        bfs_queue.pop(0)
    round += 1
#         1
#     2       3
# 4 5 6 7   8    9
#         10 11   12
#           1
#     2b 2          3r -1
# 4b 5b 6r 7b   8r 0    9b -1
#           10r 11b       12r


print("blue save", saved_blue_num)
print("red save", saved_red_num)
print("save", saved_num)
print(f'{saved_blue_num}/{saved_red_num}/{saved_num}')
#------------------------------------------------------------------
fp = open("testCase7.txt", 'r')
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
start_color = 0 # red = 1, blue = 0
bfs_queue = [1]
round = 0
while bfs_queue:
    last_level_len = len(bfs_queue)
    if round % 2 == start_color:
        bfs_queue_cp = copy.deepcopy(bfs_queue)
        select = find_max_blue_diff(bfs_queue_cp)
        update_info(select)


    else:
        bfs_queue_cp = copy.deepcopy(bfs_queue)
        select = find_max_red_diff(bfs_queue_cp)
        update_info(select)

    for i in range(last_level_len):
        for child in node_array[bfs_queue[i]].children:
            if not node_array[child].is_vaccinated:
                bfs_queue.append(child)

    saved_num += node_array[select].red_sub_nodes + node_array[select].blue_sub_nodes + 1
    saved_red_num += node_array[select].red_sub_nodes
    saved_blue_num += node_array[select].blue_sub_nodes
    if node_array[select].is_red:
        saved_red_num += 1
    else:
        saved_blue_num += 1
    if bfs_queue.count(select) != 0:
        bfs_queue.remove(select)

    for i in range(last_level_len):
        bfs_queue.pop(0)
    round += 1
#         1
#     2       3
# 4 5 6 7   8    9
#         10 11   12
#           1
#     2b 2          3r -1
# 4b 5b 6r 7b   8r 0    9b -1
#           10r 11b       12r


print("blue save", saved_blue_num)
print("red save", saved_red_num)
print("save", saved_num)
print(f'{saved_blue_num}/{saved_red_num}/{saved_num}')
#------------------------------------------------------------------
fp = open("testCase8.txt", 'r')
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
start_color = 0 # red = 1, blue = 0
bfs_queue = [1]
round = 0
while bfs_queue:
    last_level_len = len(bfs_queue)
    if round % 2 == start_color:
        bfs_queue_cp = copy.deepcopy(bfs_queue)
        select = find_max_blue_diff(bfs_queue_cp)
        update_info(select)


    else:
        bfs_queue_cp = copy.deepcopy(bfs_queue)
        select = find_max_red_diff(bfs_queue_cp)
        update_info(select)

    for i in range(last_level_len):
        for child in node_array[bfs_queue[i]].children:
            if not node_array[child].is_vaccinated:
                bfs_queue.append(child)

    saved_num += node_array[select].red_sub_nodes + node_array[select].blue_sub_nodes + 1
    saved_red_num += node_array[select].red_sub_nodes
    saved_blue_num += node_array[select].blue_sub_nodes
    if node_array[select].is_red:
        saved_red_num += 1
    else:
        saved_blue_num += 1
    if bfs_queue.count(select) != 0:
        bfs_queue.remove(select)

    for i in range(last_level_len):
        bfs_queue.pop(0)
    round += 1
#         1
#     2       3
# 4 5 6 7   8    9
#         10 11   12
#           1
#     2b 2          3r -1
# 4b 5b 6r 7b   8r 0    9b -1
#           10r 11b       12r


print("blue save", saved_blue_num)
print("red save", saved_red_num)
print("save", saved_num)
print(f'{saved_blue_num}/{saved_red_num}/{saved_num}')
#------------------------------------------------------------------
fp = open("testCase9.txt", 'r')
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
start_color = 0 # red = 1, blue = 0
bfs_queue = [1]
round = 0
while bfs_queue:
    last_level_len = len(bfs_queue)
    if round % 2 == start_color:
        bfs_queue_cp = copy.deepcopy(bfs_queue)
        select = find_max_blue_diff(bfs_queue_cp)
        update_info(select)


    else:
        bfs_queue_cp = copy.deepcopy(bfs_queue)
        select = find_max_red_diff(bfs_queue_cp)
        update_info(select)

    for i in range(last_level_len):
        for child in node_array[bfs_queue[i]].children:
            if not node_array[child].is_vaccinated:
                bfs_queue.append(child)

    saved_num += node_array[select].red_sub_nodes + node_array[select].blue_sub_nodes + 1
    saved_red_num += node_array[select].red_sub_nodes
    saved_blue_num += node_array[select].blue_sub_nodes
    if node_array[select].is_red:
        saved_red_num += 1
    else:
        saved_blue_num += 1
    if bfs_queue.count(select) != 0:
        bfs_queue.remove(select)

    for i in range(last_level_len):
        bfs_queue.pop(0)
    round += 1
#         1
#     2       3
# 4 5 6 7   8    9
#         10 11   12
#           1
#     2b 2          3r -1
# 4b 5b 6r 7b   8r 0    9b -1
#           10r 11b       12r


print("blue save", saved_blue_num)
print("red save", saved_red_num)
print("save", saved_num)
print(f'{saved_blue_num}/{saved_red_num}/{saved_num}')
#------------------------------------------------------------------
fp = open("testCase10.txt", 'r')
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
start_color = 0 # red = 1, blue = 0
bfs_queue = [1]
round = 0
while bfs_queue:
    last_level_len = len(bfs_queue)
    if round % 2 == start_color:
        bfs_queue_cp = copy.deepcopy(bfs_queue)
        select = find_max_blue_diff(bfs_queue_cp)
        update_info(select)


    else:
        bfs_queue_cp = copy.deepcopy(bfs_queue)
        select = find_max_red_diff(bfs_queue_cp)
        update_info(select)

    for i in range(last_level_len):
        for child in node_array[bfs_queue[i]].children:
            if not node_array[child].is_vaccinated:
                bfs_queue.append(child)

    saved_num += node_array[select].red_sub_nodes + node_array[select].blue_sub_nodes + 1
    saved_red_num += node_array[select].red_sub_nodes
    saved_blue_num += node_array[select].blue_sub_nodes
    if node_array[select].is_red:
        saved_red_num += 1
    else:
        saved_blue_num += 1
    if bfs_queue.count(select) != 0:
        bfs_queue.remove(select)

    for i in range(last_level_len):
        bfs_queue.pop(0)
    round += 1
#         1
#     2       3
# 4 5 6 7   8    9
#         10 11   12
#           1
#     2b 2          3r -1
# 4b 5b 6r 7b   8r 0    9b -1
#           10r 11b       12r


print("blue save", saved_blue_num)
print("red save", saved_red_num)
print("save", saved_num)
print(f'{saved_blue_num}/{saved_red_num}/{saved_num}')
