from lib.BWMatching import gen_count, gen_first_occurrence, bw_matching
from lib.MultiplePatternMatching import gen_suffix_array_and_last_column

def find_in_last_column(last_column, symbol, l):
  s = 0
  e = len(last_column[symbol])
  N = e

  while s < e:
    m = (s + e) // 2

    if last_column[symbol][m] >= l:
      e = m
    else:
      s = m + 1
  
  return s

def multiple_approximate_pattern_matching(Text, patterns, d):
  Text = Text + "$"
  print(Text)
  suffix_array, last_column = gen_suffix_array_and_last_column(Text)
  first_occurrence = gen_first_occurrence(last_column)
  count = gen_count(last_column)
  print(last_column)

  ress = {}
  for pattern in patterns:
    n = len(pattern)
    k = int( n / (d + 1))
    ress[pattern] = []

    for s in range(n - k + 1):
      sub_pattern = pattern[s:s+k]
      sub_d = 0
      prefix = s
      suffix = s+k-1

      top, bottom = bw_matching(first_occurrence, last_column, sub_pattern, count)
      print(pattern, sub_pattern, s, s+k-1, '|', top, bottom)
      
      for index in range(top, bottom+1):
        sub_pattern = pattern[s:s+k]

        # elongate prefix
        prefix = s
        symbol = pattern[prefix] # 바로 앞 문자
        while prefix >= 0 and sub_d <= d:
          # pattern의 앞 문자 획득
          prefix -= 1
          symbol = pattern[prefix]
          if symbol == '$':
            break

          # text의 앞 문자 획득
          text_symbol = last_column[index]
          index -= 1

          if text_symbol != symbol:
            sub_d += 1
          
          print(symbol, text_symbol, prefix, sub_d, index)

          # top = first_occurrence[symbol] + count[symbol][top]
          # if symbol != last_column[top]:
          #   sub_d += 1
          #   sub_pattern = last_column[top] + sub_pattern
          #   if sub_d > d:
          #     break
          # prefix -= 1
          # symbol = last_column[top]
          # sub_pattern = symbol + sub_pattern

        # elongate suffix
        # symbol = sub_pattern[-1]
        # while suffix < n and sub_d < d:
        #   bottom = first_occurrence[symbol] + count[symbol][bottom]
        #   if symbol != last_column[bottom]:
        #     sub_d += 1
        #     if sub_d < d:
        #       break
        #   suffix += 1
        #   symbol = last_column[bottom]
        
        if suffix == n-1 and prefix == 0:
          print('add\t', sub_pattern, prefix, suffix, s, n-k, index, suffix_array[index], text[index-len(pattern)+1:index+1])
          ress[pattern].append(suffix_array[index])

  return ress

fn = "1 copy.txt"
f = open(f"./data/{fn}")
text = f.readline().strip()
patterns = f.readline().strip().split()
d = int(f.readline().strip())
f.close()

ress = multiple_approximate_pattern_matching(text, patterns, d)

fn = "output.txt"
f = open(f"./data/{fn}", "w")
for key, res in ress.items():
  s = " ".join(list(map(str, res)))
  f.write(f"{key}: {s}\n")
  print(f"{key}: {s}")
f.close()