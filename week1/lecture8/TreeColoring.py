def tree_coloring(colored_tree):
  L = len(colored_tree)
  color_index = {'gray': 0, 'blue': 1, 'red': 2, 'purple': 3}

  while True:
    isColored = False
    for i in range(L):

      if colored_tree[i][1] == 'gray':
        children_color = [0, 0, 0, 0]
        for next in colored_tree[i][0]:
          child_color = colored_tree[next][1]
          children_color[ color_index[child_color] ] += 1
        
        num_color = sum(children_color[1:])
        if children_color[0] == 0 and num_color > 0:
          if num_color == children_color[1]:
            colored_tree[i][1] = 'blue'
            isColored = True
          elif num_color == children_color[2]:
            colored_tree[i][1] = 'red'
            isColored = True
          else:
            colored_tree[i][1] = 'purple'
            isColored = True

    if not isColored:
      break

  colors = [f"{i}: {colored_tree[i][1]}" for i in range(L)]
  
  return colors

fn = "dataset_9665_6 (2).txt"
f = open(f"./data/{fn}")
Tree = []

isEdgeReading = True
while True:
  line = f.readline().strip()

  if not line:
    break
  if line == '-':
    isEdgeReading = False
    continue

  if isEdgeReading:
    cur, next = line.split(':')

    if not next:
      Tree.append([ [], 'gray'])
    else:
      nexts = list(map(int, next.strip().split()))
      Tree.append([nexts, 'gray'])
  else:
    node, color = line.split()
    Tree[int(node)][1] = color

ress = tree_coloring(Tree)
for res in ress:
  print(res)
