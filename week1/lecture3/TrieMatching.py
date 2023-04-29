from PrefixTrieMatching import prefix_trie_matching
from TrieConstruction import trie_construction

def trie_matching(text, trie):
  ress = {}

  for i in range(len(text)):
    res = prefix_trie_matching(text[i:], trie)

    if res:
      if not ress.get(res):
        ress[res] = [i]
      else:
        ress[res].append(i)
  
  return ress



fn = "dataset_294_8.txt"
f = open(f"./data/{fn}")
text = f.readline().strip()
patterns = f.readline().strip().split()
trie = trie_construction(patterns)
print(trie)
ress = trie_matching(text, trie)
for pattern, indices in ress.items():
  print(f"{pattern}:", end=" ")
  print(" ".join(list(map(str, indices))))