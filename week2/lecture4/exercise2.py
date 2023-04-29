from collections import deque

data = "TTACA$AAGTC"

s = list(data)
e = list(data)
s.sort()
# print("".join(s))
# print("".join(e))


N = len(s)

echarseq2ei = {}
si2scharseq = {}
scharseq = {}

for i in range(N):
  e_char = e[i]
  s_char = s[i]


  if echarseq2ei.get(e_char):
    echarseq2ei[e_char].append(i)
  else:
    echarseq2ei[e_char] = [i]
  
  if scharseq.get(s_char) != None:
    scharseq[s_char] += 1
    si2scharseq[i] = [s_char, scharseq[s_char]]
  else:
    scharseq[s_char] = 0
    si2scharseq[i] = [s_char, scharseq[s_char]]

# print(echarseq2ei)
# print(si2scharseq)
# print(scharseq)
arr = []
char_seq = 0
cur_e = '$'

# while cur_e != '$':
while True:
  # print(cur_e, char_seq)
  cur_e = echarseq2ei[cur_e][char_seq]
  [cur_e, char_seq] = si2scharseq[cur_e]
  arr.append(cur_e)
  if cur_e == '$':
    break
print("".join(arr))