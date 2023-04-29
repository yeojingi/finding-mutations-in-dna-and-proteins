from ModifiedSuffixTreeConstruction import modified_suffix_tree_construction
from TreeColoring import tree_coloring

def shortest_non_shared_substring(Text1, Text2):
  # generate Trie
  Trie = modified_suffix_tree_construction(Text1 + "#" + Text2 + "$")
  # for i in range(len(Trie)):
  #   print(i, Trie[i])
  print("Trie generated")

  # color
  colored_tree = [ [[], "gray"] for _ in range(len(Trie))]
  for i in range(len(Trie)):
    for k in Trie[i].keys():
      for e_k in k:
        e = Trie[i][e_k][0]

        colored_tree[i][0].append(e)

        if e_k == '$':
          colored_tree[e][1] = "red"
        elif e_k == '#':
          colored_tree[e][1] = "blue"
  
  colors = [colored_tree[i][1] for i in range(len(colored_tree))]
  
  colors = tree_coloring(colored_tree)
  print('color tree generated')
  # only trace purple line
  shortest = list(Text1+Text2)

  s = [ [0, []] ]
  while s:
    [cur, track] = s.pop()
    # print(cur, track)

    for next_symbol, next_node in Trie[cur].items():
      [next_i, _] = next_node

      if colors[next_i] == 'purple':
        s.append([next_i, track + [next_symbol]])
      elif colors[next_i] != 'purple' and (next_symbol != '$' and next_symbol != '#'):
        if len(track) + 1 < len(shortest):
          shortest = track + [next_symbol]

  
  # save the longest
  # return
  return "".join(shortest)

fn = "dataset_296_7.txt"
f = open(f"./data/{fn}")
Text1 = f.readline().strip()
Text2 = f.readline().strip()
res = shortest_non_shared_substring(Text1, Text2)
print(res)