def occur(top, bottom, last_column, symbol):
  for i in range(top, bottom+1):
    if last_column[i] == symbol:
      return True
  return False

def better_bw_matching(first_occurrence, last_column, pattern, count):
  top = 0
  bottom = len(last_column) - 1

  while top <= bottom:
    if len(pattern) > 0:
      symbol = pattern[-1]
      pattern = pattern[:-1]
      if occur(top, bottom, last_column, symbol):
        top = first_occurrence[symbol] + count[symbol][top]
        bottom = first_occurrence[symbol] + count[symbol][bottom+1] - 1
      else:
        return 0
    else:
      return bottom - top + 1

def gen_first_occurrence(text):
  firstColumn = list(text)
  firstColumn.sort()

  first_occurrence = {}

  N = len(text)

  for i in range(N):
    chr = firstColumn[i]

    if not first_occurrence.get(chr):
      first_occurrence[chr] = i
  
  return first_occurrence

def gen_count(text):
  N = len(text)
  chrs = list(set(text))

  count = { chr: [0] * (N+1) for chr in chrs}
  
  for i in range(1, N+1):
    for chr in chrs:
      if chr == text[i-1]:
        count[chr][i] = count[chr][i-1] + 1
      else:
        count[chr][i] = count[chr][i-1]

  return count


fn = "2.txt"
f = open(f"./data/{fn}")
text = f.readline().strip()
patterns = f.readline().strip().split()
first_occurrence = gen_first_occurrence(text)
count = gen_count(text)

res = []
for pattern in patterns:
  print(first_occurrence)
  print(count)
  n = better_bw_matching(first_occurrence, text, pattern, count)
  res.append(n)

print(*res, sep=" ")