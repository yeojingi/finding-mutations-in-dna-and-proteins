def modified_suffix_tree_construction(Text):
  Trie = [{}]
  for i in range(len(Text)):
    current_node_i = 0
    for j in range(i, len(Text)):
      current_symbol = Text[j]
      if Trie[current_node_i].get(current_symbol):
        current_node_i = Trie[current_node_i][current_symbol][0]
      else:
        Trie.append({})
        Trie[current_node_i][current_symbol] = [len(Trie)-1, j]
        current_node_i = len(Trie)-1
    
    # if len(Trie[current_node_i]) == 0:
    #   Trie.append({})
    #   Trie[current_node_i]['$'] = [len(Trie)-1, i]
  
  n = 0
  for i in range(len(Trie)):
    for k, v in Trie[i].items():
      if k == '$':
        n+=1
  print(n)

  return Trie

def suffix_tree_construction(Text):
  Trie = modified_suffix_tree_construction(Text)
  # for i in range(len(Trie)):
  #   print(i, Trie[i])
  traces = []

  def traverse(cur, track):
    if len(Trie[cur]) == 1:
      for symbol, next_index in Trie[cur].items():
        next = next_index[0]
        index = next_index[1]

        traverse(next, track + symbol)
      return
    elif len(Trie[cur]) == 0:
      traces.append(track)
      # print(track, cur, "0")
      return 
    else:
      if len(track) > 0:
        traces.append(track)
        track = ""

      for symbol, next_index in Trie[cur].items():
        next = next_index[0]
        index = next_index[1]

        traverse(next, symbol)

  traverse(0, "")

  return traces
      

fn = "quiz.txt"
f = open(f"./data/{fn}")
Text = f.readline().strip()
ress = suffix_tree_construction(Text)
f.close()

fon = "output.txt"
fo = open(f"./data/{fon}", "w")
for res in ress:
  fo.write(f"{res} ")
# print(*res, sep=" ")