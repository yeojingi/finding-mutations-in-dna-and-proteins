def burrows_wheeler_transform_construction(Text):
    matrix = []

    for i in range(len(Text)):
        tmp = Text[i:] + Text[:i]
        matrix.append(tmp)
    
    matrix.sort()

    res = []

    for i in range(len(matrix)):
        res.append(matrix[i][-1])
    
    return "".join(res)

fn = "dataset_297_5.txt"
f = open(f"./data/{fn}")
Text = f.readline().strip()
res = burrows_wheeler_transform_construction(Text)
print(res)