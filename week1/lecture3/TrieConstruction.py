def trie_construction(patterns):
  Trie = [ {} ]

  for pattern in patterns:
    current_node = 0
    for i in range(len(pattern)):
      current_symbol = pattern[i]

      if Trie[current_node].get(current_symbol):
        current_node = Trie[current_node][current_symbol]
      else:
        Trie.append({})
        Trie[current_node][current_symbol] = len(Trie) - 1
        current_node = len(Trie) - 1
  
  return Trie
  # edges = []

  # for i in range(len(Trie)):
  #   for symbol, node in Trie[i].items():
  #     edges.append([i, node, symbol])

  # return edges

# fn = "dataset_294_4.txt"
# f = open(f"./data/{fn}")
# patterns = f.readline().strip().split()
# ress = trie_construction(patterns)

# fon = "output.txt"
# fo = open(f"./data/{fon}", "w")
# for res in ress:
#   fo.write(f"{res[0]} {res[1]} {res[2]}\n")
# fo.close()