def print_result(states, paths, pockets):
  print(' ', end="")
  for state in states:
    print(state, end=" ")
  print()
  for key, val in paths.items():
    denom = sum(val.values())
    print(key, end=" ")

    for s in val.values():
      if denom > 0 and s > 0:
        print(s/denom, end=" ")
      else:
        print(0, end=" ")

    print()
  print("--------")

  print(' ', end="")
  for char in chars:
    print(char, end=" ")
  print()
  for key, val in pockets.items():
    denom = sum(val.values())
    print(key, end=" ")

    for s in val.values():
      if denom > 0 and s > 0:
        # print("{:.3f}".format(s/denom), end="\t")
        print(s/denom, end=" ")
      else:
        print(0, end=" ")

    print()

def profile_hmm_with_pseudo_count(theta, pseudo_count, chars, alignments):
  # find indecies where the missing chars are greater or equal than theta
  M = len(alignments)
  L = len(alignments[0])


  indices = [0] * L
  latest_index = 0

  for l in range(L):
    num_space = 0
    for m in range(M):
      if alignments[m][l] == '-':
        num_space += 1
    
    if num_space / M >= theta:
      indices[l] = -1
    else:
      latest_index += 1
      indices[l] = latest_index

  N = latest_index

  states = ['S', 'I0']
  for i in range(1, N+1):
    states.append(f'M{i}')
    states.append(f'D{i}')
    states.append(f'I{i}')
  states.append('E')

  pockets = { state: {char: 0 for char in chars} for state in states}
  paths = { state: {state2: 0.0 for state2 in states} for state in states}
  
  for m in range(M):
    latest_index = 0
    insert_or_delete = False
    inserteds = []
    prev_state = 'S'
    
    alignment = alignments[m]
    for l in range(L):
      if indices[l] > 0:
        if insert_or_delete:
          if inserteds:
            cur_state = f"I{latest_index}"

            for char in inserteds:
              pockets[cur_state][char] += 1

              paths[prev_state][cur_state] += 1
              prev_state = cur_state

          insert_or_delete = False
          inserteds = []

        index = indices[l]
        latest_index = index
        char = alignment[l]

        if char == '-':
          cur_state = f'D{index}'
        else:
          cur_state = f'M{index}'
          pockets[cur_state][char] += 1

        paths[prev_state][cur_state] += 1
        prev_state = cur_state
      else:
        insert_or_delete = True

        char = alignment[l]
        if char != '-':
          inserteds.append(char)
    
    if insert_or_delete:
      if inserteds:
        cur_state = f"I{latest_index}"

        for char in inserteds:
          pockets[cur_state][char] += 1

          paths[prev_state][cur_state] += 1
          prev_state = cur_state

      insert_or_delete = False
      inserteds = []
    paths[prev_state]['E'] += 1

  # normalize
  for key, val in paths.items():
    denom = sum(val.values())
    for v in val.keys():
      if denom != 0:
        val[v] = val[v]/denom
  for key, val in pockets.items():
    denom = sum(val.values())
    for v in val.keys():
      if denom != 0:
        val[v] = val[v]/denom

  # pseudo_count for path
  for key, val in paths.items():
    i = key[-1]
    to_explore = 0

    if i == 'S':
      i = 0
      to_explore = [f"I{i}", f"M{i+1}", f"D{i+1}"]
    elif i == 'E':
      continue
    else:
      i = int(i)
      to_explore = [f"I{i}", f"M{i+1}", f"D{i+1}"]

      if i == N:
        to_explore = [f"I{i}", "E"]
    
    for v in to_explore:
      paths[key][v] += pseudo_count

  # pseudo_count for pocket
  for key, val in pockets.items():
    if key[0] in ["I", "M"]:
      for s in val:
        val[s] += pseudo_count


  for key, val in paths.items():
    denom = sum(val.values())

    for s in val.keys():
      if denom > 0 and val[s] > 0:
        val[s] = val[s]/denom

  for key, val in pockets.items():
    denom = sum(val.values())

    for s in val.keys():
      if denom > 0 and val[s] > 0:
        val[s] = val[s]/denom

  return N, states, paths, pockets

def sequence_alignment_with_profile_hmm(string, theta, pseudo_count, chars, alignments):
  N, states, paths, pockets = profile_hmm_with_pseudo_count(theta, pseudo_count, chars, alignments)

  M = len(alignments)
  L = len(alignments[0])
  S = len(string)

  dp = [ {} for _ in range(S+2) ]
  track = [ {} for _ in range(S+2) ]

  for n in range(S+2):
    if n == 0:
      eles = ['S'] + [ f"D{i+1}" for i in range(N) ]
      
      prev_ele = 'S'
      k = -1
      for ele in eles:
        if ele == 'S':
          dp[n][ele] = 1
          track[n][ele] = []
        else:
          # D
          dp[n][ele] = dp[n][prev_ele] * paths[prev_ele][ele]
          track[n][ele] = track[n][prev_ele] + [ele]
        prev_ele = ele
        k += 1

    elif n == S+1:
      dp[n]['E'] = 0
      track[n]['E'] = []
    else:
      eles = [0] * (3*N + 1)
      eles[0] = f"I{0}"
      for i in range(N):
        eles[1 + 3*i] = f"M{i+1}"
        eles[1 + 3*i+1] = f"D{i+1}"
        eles[1 + 3*i+2] = f"I{i+1}"
      for ele in eles:
        dp[n][ele] = 0
        track[n][ele] = []
    
  for i in range(1, S+1):
    prev_nodes = dp[i-1].keys()
    nodes = dp[i].keys()

    chr = string[i-1]

    for node in nodes:

      # TODO: node의 종류에 따라 prev_nodes를 바꾸면 됨
      # 지금은 모든 이전 노드를 보는데 https://bioinformaticsalgorithms.com/images/HMM/profile_HMM_Viterbi_complete.png
      # 위 이미지에 맞게 적당한 노드만 탐색하면 해결될 듯ㅈ
      # if node == ''
      h = int(node[1])
      if node[0] == 'D':
        if h == 1:
          if dp[i][node] < dp[i]['I0'] * paths['I0']['D1']:
            dp[i][node] = dp[i]['I0'] * paths['I0']['D1']
            track[i][node] = track[i]['I0'] + ['D1']
        else:
          prev_nodes = [f"M{h-1}", f"D{h-1}", f"I{h-1}"]
          for prev_node in prev_nodes:
            e = dp[i][prev_node] * paths[prev_node][node]

            if dp[i][node] < e:
              dp[i][node] = e
              track[i][node] = track[i][prev_node] + [node]
      elif node[0] == 'M':
        if h == 1:
          prev_nodes = ["I0"]
        else:
          prev_nodes = [f"M{h-1}", f"D{h-1}", f"I{h-1}"]

        if i == 1:
          prev_nodes.append("S")

        for prev_node in prev_nodes:
          if i == 1 and (prev_node[0] == "I" or prev_node[0] == 'M'):
            continue

          e = dp[i-1][prev_node] * paths[prev_node][node] * pockets[node][chr]

          if dp[i][node] < e:
            dp[i][node] = e
            track[i][node] = track[i-1][prev_node] + [node]
      elif node[0] == 'I':
        if h == 0:
          prev_nodes = ["I0"]
        else:
          prev_nodes = [f"M{h}", f"D{h}", f"I{h}"]

        if i == 1:
          prev_nodes.append("S")

        for prev_node in prev_nodes:
          if i == 1 and (prev_node[0] == "I" or prev_node[0] == 'M'):
            continue
          e = dp[i-1][prev_node] * paths[prev_node][node] * pockets[node][chr]

          if dp[i][node] < e:
            dp[i][node] = e
            track[i][node] = track[i-1][prev_node] + [node]


      # for prev_node in prev_nodes:
      #   e = dp[i-1][prev_node] * paths[prev_node][node]

      #   if node[0] != 'D':
      #     e *= pockets[node][chr]
      #   else:
      #     h = int(node[1])
      #     if h == 1:
      #       if dp[i][node] < dp[i]['I0'] * paths['I0']['D1']:
      #         dp[i][node] = dp[i]['I0'] * paths['I0']['D1']
      #         track[i][node] = track[i]['I0'] + ['D1']
      #     else:
      #       for l in [f"M{h-1}", f"D{h-1}", f"I{h-1}"]:
      #         if dp[i][node] < dp[i][l] * paths[l][node] :
      #           dp[i][node] = dp[i][l] * paths[l][node]
      #           track[i][node] = track[i][l] + [node]
      #         # dp[i][node] = max(dp[i][node], dp[i][l] * paths[l][node])

      #   if dp[i][node] < e:
      #     dp[i][node] = e
      #     # print(prev_node, i)
      #     track[i][node] = track[i-1][prev_node] + [node]

  # print_result(states, paths, pockets)
  print(*dp, sep="\n")
  # print()
  # print(*track, sep="\n")
  res = []
  res_prob = 0
  for a in [f"M{N}", f"D{N}", f"I{N}"]:
    if dp[S][a] > res_prob:
      res_prob = dp[S][a]
      res = track[S][a]

  return " ".join(res)

fn = "dataset_26259_14.txt"
# f = open(f"./data/{fn}")
f = open(f"./data/07_ProfileHmmAlignment/inputs/{fn}")

string = f.readline().strip()
f.readline()

theta, pseudo_count = map(float, f.readline().strip().split())
f.readline()

chars = f.readline().strip().split()
f.readline()

alignments = []
while True:
  line = f.readline().strip()

  if not line:
    break

  alignments.append(line)

res = sequence_alignment_with_profile_hmm(string, theta, pseudo_count, chars, alignments)
print(res)