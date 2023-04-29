def prefix_trie_matching(text, trie):
  # print(text, trie)
  symbol = text[0]
  i_t = 0
  v = 0

  track = []

  while i_t <= len(text):
    if not trie[v]:
      return "".join(track)
    elif i_t < len(text) and trie[v].get( text[i_t] ):
      symbol = text[i_t]
      v = trie[v][symbol]
      track.append(symbol)
      i_t += 1
    else:
      # print('false', i_t, symbol, v)
      return False
    
  return False
