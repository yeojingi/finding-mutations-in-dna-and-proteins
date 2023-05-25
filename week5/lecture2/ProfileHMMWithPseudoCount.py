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

  return

fn = "2.txt"
f = open(f"./data/{fn}")

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

res = profile_hmm_with_pseudo_count(theta, pseudo_count, chars, alignments)
# print(res)