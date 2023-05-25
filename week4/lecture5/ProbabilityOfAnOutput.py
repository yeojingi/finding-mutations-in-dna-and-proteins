def probability_with_a_hidden_path(string, characters, path, states, matrix):
  prob = 1

  for i in range(len(string)):
    influx = path[i]
    efflux = string[i]

    prob *= matrix[influx][efflux]

  return prob

fn = "dataset_26255_10.txt"
f = open(f"./data/{fn}")

string = f.readline().strip()
f.readline().strip()

characters = f.readline().strip().split()
f.readline().strip()

path = f.readline().strip()
f.readline().strip()

states = f.readline().strip().split()
f.readline().strip()

headers = f.readline().strip().split()

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
    matrix[fr][headers[i]] = float(values[i])

res = probability_with_a_hidden_path(string, characters, path, states, matrix)
print(res)