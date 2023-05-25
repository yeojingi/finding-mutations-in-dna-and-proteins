def profile_hmm(theta, chars, alignments):
  # find indecies where the missing chars are greater or equal than theta
  M = len(alignments)
  L = len(alignments[0])

  over_theta_indices = []
  charI_to_refI = {i: i+1 for i in range(L)}

  for l in range(L):
    num_space = 0
    for m in range(M):
      if alignments[m][l] == '-':
        num_space += 1
    
    if num_space / M >= theta:
      over_theta_indices.append(l)

      if l > 0:
        charI_to_refI[l] = charI_to_refI[l-1]
      else:
        charI_to_refI[l] = 0
  
  
  N = L - len(over_theta_indices)

  states = ['S', 'I0']
  for i in range(1, N+1):
    states.append(f'M{i}')
    states.append(f'D{i}')
    states.append(f'I{i}')
  states.append('E')
  
  edges = { state: {state: [] for state in states} for state in states}
  print(charI_to_refI)

  for m in range(M):
    path = ['S']
    alignment = alignments[m]
    inserted = 0

    for l in range(L):
      i = charI_to_refI[l]

      if l in over_theta_indices:
        if path[-1] == f'I{i}':
          continue
        
        if alignment[l] != '-':
          path.append(f"I{i}")

      else:
        if alignment[l] == '-':
          path.append(f"D{i}")
    path.append('E')
    print(path, alignment)

  return

fn = "1.txt"
f = open(f"./data/{fn}")

theta = float(f.readline().strip())
f.readline()

chars = f.readline().strip().split()
f.readline()

alignments = []
while True:
  line = f.readline().strip()

  if not line:
    break

  alignments.append(line)

res = profile_hmm(theta, chars, alignments)
print(res)