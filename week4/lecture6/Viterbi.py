def viterbi(string, characters, states, transition, emission):
  dp = [ [0] * len(string) for _ in range(len(states)) ]
  state_dp = [ [""] * len(string) for _ in range(len(states))]

  for i in range(len(states)):
    dp[i][0] = 1/2 * emission[states[i]][string[0]]
    state_dp[i][0] = states[i]

  for j in range(1, len(string)):
    for i in range(len(states)):
      cur_state = states[i]
      chr = string[j]

      max_value = 0
      max_state = 0
      for k in range(len(states)):
        state = states[k]

        value = dp[k][j-1] * emission[cur_state][chr] * transition[state][cur_state]

        if value > max_value:
          max_value = value
          max_state = k
      
      dp[i][j] = max_value
      state_dp[i][j] = state_dp[max_state][j-1] + cur_state

  max_path = ""
  max_prob = 0
  for i in range(len(states)):
    if dp[i][-1] > max_prob:
      max_prob = dp[i][-1]
      max_path = state_dp[i][-1]
  return "".join(max_path)


fn = "2.txt"
f = open(f"./data/{fn}")

string = f.readline().strip()
f.readline().strip()

characters = f.readline().strip().split()
f.readline().strip()

states = f.readline().strip().split()
f.readline().strip()

transition = {}
headers = f.readline().strip().split()
while True:
  line = f.readline().strip()

  if line[0] == '-':
    break

  tokens = line.split()
  prev = tokens[0]
  values = tokens[1:]
  transition[prev] = {}
  for i in range(len(values)):
    chr = headers[i]
    transition[prev][chr] = float(values[i])

emission = {}
headers = f.readline().strip().split()
while True:
  line = f.readline().strip()

  if not line:
    break

  tokens = line.split()
  prev = tokens[0]
  values = tokens[1:]
  emission[prev] = {}
  for i in range(len(values)):
    chr = headers[i]
    emission[prev][chr] = float(values[i])

res = viterbi(string, characters, states, transition, emission)
print(res)