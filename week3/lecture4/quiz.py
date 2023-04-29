from lib.MultiplePatternMatching import gen_suffix_array_and_last_column

t = "banana$"
suffix_array, last_column = gen_suffix_array_and_last_column(t)
print(" ".join(list(map(str, suffix_array))))