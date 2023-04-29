def suffix_array(Text):
    token2index = {}
    tokens = []

    for i in range(len(Text)):
        token2index[Text[i:]] = i
        tokens.append(Text[i:])

    tokens.sort()

    indecies = [0] * len(tokens)

    for i in range(len(tokens)):
        token = tokens[i]
        indecies[i] = token2index[token]
    
    return indecies

fn = "dataset_310_2.txt"
f = open(f"./data/{fn}")
Text = f.readline().strip()
ress = suffix_array(Text)
print(*ress, sep=" ")