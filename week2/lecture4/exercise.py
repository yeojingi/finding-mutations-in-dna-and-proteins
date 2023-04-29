from collections import deque

s = list('enwvpeoseu$llt')
e = list('enwvpeoseu$llt')
s.sort()
print("".join(s))
print("".join(e))


N = len(s)

edge = {}

for i in range(N):
  start = e[i]
  end_s = s[i]

  # if end_s == '$':
  #   continue

  if edge.get(start):
    edge[start].append(end_s)
  else:
    edge[start] = deque([end_s])

re_s = []

for key, val in edge.items():
  if '$' in val:
    cur = key
# re_s.append(cur)
cur = edge[cur].popleft()
re_s.append(cur)
n = 1
# while cur != '$':
while n < N:
  cur = edge[cur].popleft()
  re_s.append(cur)
  print("".join(re_s))
  n+=1

re_s.reverse()
print("".join(re_s))
