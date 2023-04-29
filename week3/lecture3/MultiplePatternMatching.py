from BWMatching import gen_count, gen_first_occurrence, bw_matching

def gen_suffix_array_and_last_column(text, K):
  offset_arr = []
  N = len(text)

  for i in range(N):
    arranged_text = text[i:] + text[:i]
    offset_arr.append(arranged_text)
  
  offset_arr.sort()

  text2index = { offset_arr[i]: i for i in range(len(offset_arr))}

  checkpoints = []
  suffix_array = [0] * N
  for i in range(N):
    arranged_text = text[i:] + text[:i]
    j = text2index[ arranged_text ]
    suffix_array[j] = i
    if i % K == 0:
      checkpoints.append([j, i])
  
  checkpoints.sort()

  last_column = "".join([ e[-1] for e in offset_arr])

  return suffix_array, last_column

def multiple_pattern_matching(text, patterns):
  pass

fn = "dataset_303_4 (1).txt"
f = open(f"./data/{fn}")
text = f.readline().strip() + "$"
patterns = f.readline().strip().split()

suffix_array, last_column = gen_suffix_array_and_last_column(text, 5)

first_occurrence = gen_first_occurrence(last_column)
count = gen_count(last_column)

# print(last_column)
ress = []
for pattern in patterns:
  # print(first_occurrence)
  # print(count)
  top, bottom = bw_matching(first_occurrence, last_column, pattern, count)
  if top != -1 and bottom != -1:
    indices = []
    for i in range(top, bottom+1):
      indices.append(suffix_array[i])
    
    indices.sort()
    indices = " ".join(list(map(str, indices)))
  else:
    indices = ""
  ress.append(f"{pattern}: {indices}")
  # print(top, bottom, ress[-1])
f.close()

fn = 'output.txt'
f = open(f"./data/{fn}", 'w')
for res in ress:
  f.write(f"{res}\n")
# print(*ress, sep="\n")