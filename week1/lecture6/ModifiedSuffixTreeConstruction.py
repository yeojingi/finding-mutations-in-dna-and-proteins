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
    
    if len(Trie[current_node_i]) == 0:
      Trie.append({})
      Trie[current_node_i]['$'] = [len(Trie)-1, i]
  
  return Trie


# modified_suffix_tree_construction("ATAAATG$")
# modified_suffix_tree_construction("panamabananas$")