from collections import deque
import sys

sys.setrecursionlimit(10**5)

def tree_coloring(colored_tree):
  L = len(colored_tree)
  color_index = {'gray': 0, 'red': 1, 'purple': 2}

  def traverse(cur):
    if colored_tree[cur][1] == 'gray':
      for next in colored_tree[cur][0]:
        traverse(next)
    else:
      return
    
    children_color = [0, 0, 0]
    for next in colored_tree[cur][0]:
      child_color = colored_tree[next][1]
      children_color[ color_index[child_color] ] += 1
    
    num_color = sum(children_color[1:])
    if children_color[0] == 0 and num_color > 0:
      if children_color[ color_index['purple'] ] > 0 or children_color[ color_index['red'] ] > 1:
        colored_tree[cur][1] = 'purple'
      else:
        colored_tree[cur][1] = 'red'

  traverse(0)

  colors = [colored_tree[i][1] for i in range(L)]
  
  return colors
