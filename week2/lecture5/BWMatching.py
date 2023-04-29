def bw_matching(lastColumn, pattern, lastToFirst):
  top = 0
  bottom = len(lastColumn) - 1

  while top <= bottom:
    if len(pattern) > 0:
      symbol = pattern[-1]
      pattern = pattern[:-1]

      topIndex = -1
      for i in range(top, bottom+1):
        if lastColumn[i] == symbol:
          if topIndex < 0:
            topIndex = i
            bottomIndex = i
          else:
            bottomIndex = i
          
      if topIndex >= 0:
        top = lastToFirst[topIndex]
        bottom = lastToFirst[bottomIndex]
      else:
        return 0
    else:
      return bottom - top + 1

def column_builder(text):
  N = len(text)
  lastToFirst = []

  last = list(text)
  first = list(text)
  first.sort()

  # print("".join(first))
  # print("".join(last))
  
  first_str_seq_to_i = {}

  for i in range(N):
    chr = first[i]

    if first_str_seq_to_i.get(chr):
      first_str_seq_to_i[chr].append(i)
    else:
      first_str_seq_to_i[chr] = [i]

  last_str_seq_to_i = {}
  
  for i in range(N):
    chr = last[i]
    seq = 0

    if last_str_seq_to_i.get(chr):
      last_str_seq_to_i[chr].append(i)
    else:
      last_str_seq_to_i[chr] = [i]
    
    seq = len(last_str_seq_to_i[chr]) - 1
    
    # print(seq, first_str_seq_to_i[chr])
    lastToFirst.append(first_str_seq_to_i[chr][seq])
  
  return lastToFirst

fn = "dataset_300_8.txt"
f = open(f"./data/{fn}")
text = f.readline().strip()
patterns = f.readline().strip().split()
lastToFirst = column_builder(text)

res = []

for pattern in patterns:
  i = bw_matching(text, pattern, lastToFirst)
  res.append(i)

print(" ".join(list(map(str, res))))