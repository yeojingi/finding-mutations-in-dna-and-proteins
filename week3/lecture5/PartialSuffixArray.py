def partial_suffix_array(text, K):
  offset_arr = []
  text2index = {}
  N = len(text)

  for i in range(N):
    arranged_text = text[i:] + text[:i]
    offset_arr.append(arranged_text)
  
  offset_arr.sort()

  text2index = { offset_arr[i]: i for i in range(len(offset_arr))}

  # for i in range(len(offset_arr)):
  #   print(i, offset_arr[i], text2index[offset_arr[i]])
  # print(*offset_arr, sep="\n")

  suffix_array = []
  for i in range(0, N, K):
    arranged_text = text[i:] + text[:i]
    j = text2index[ arranged_text ]
    suffix_array.append([j, i])
  
  suffix_array.sort()

  return suffix_array

fn = "dataset_9809_2.txt"
f = open(f"./data/{fn}")
text = f.readline().strip()
K = int(f.readline().strip())
arr = partial_suffix_array(text, K)
arr.sort()
f.close()

fn = 'output.txt'
f = open(f"./data/{fn}", 'w')
for e in arr:
  s = " ".join(list(map(str, e)))
  f.write(f"{s}\n")

f.close()