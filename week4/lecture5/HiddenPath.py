def hidden_path(path, states, matrix):
  prev = path[0]

  val = 1 / len(states)

  for i in range(1, len(path)):
    cur = path[i]

    val *= matrix[prev][cur]
    prev = cur
  
  return val

fn = "dataset_26255_8.txt"
f = open(f"./data/{fn}")

path = f.readline().strip()
f.readline()

states = f.readline().strip().split()
f.readline()

header = f.readline().strip().split()

matrix = {}
while True:
  line = f.readline().strip()

  if not line:
    break

  tokens = line.split()
  fr = tokens[0]
  values = tokens[1:]

  matrix[fr] = {}

  for i in range(len(values)):
    matrix[fr][header[i]] = float(values[i])

res = hidden_path(path, states, matrix)
print(res)