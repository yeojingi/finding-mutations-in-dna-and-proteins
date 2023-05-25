from itertools import product

emission = {
  "F": {'H': 1/2, 'T': 1/2},
  "B": {'H': 3/4, 'T': 1/4}
}

transition = {
  'F': {'F': 9/10, 'B': 1/10},
  'B': {'F': 1/10, 'B': 9/10}
}

chars = ['F', 'B']
perms = list(product(chars, chars, chars, chars))

reference = ['H', 'H', 'T', 'T']

best_perm = perms[0]
best_prob = 0
for perm in perms:
  prob = 1/2
  chr = perm[0]
  chr_ref = reference[0]
  prob *= emission[chr][chr_ref]

  chr_prev = chr

  for i in range(1, len(perm)):
    chr = perm[i]
    chr_ref = reference[i]

    prob *= emission[chr][chr_ref]
    prob *= transition[chr_prev][chr]

    chr_prev = chr
  
  if prob > best_prob:
    best_prob = prob
    best_perm = perm

print("".join(best_perm))