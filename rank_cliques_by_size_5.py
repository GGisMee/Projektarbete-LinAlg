#from partition_cliques_4.py import list

#Lista för att testa
a = ["a", "b", "c"]
b = ["d", "e", ""]
c = ["f"]
d = ["g", "h", "i", "j"]
temp_list = [a, b, c, d]

def find_index_longest(v):
    #Hittar index för längsta listan i lista v, returnerar index
    index_max = 0
    for i in range(len(v)):
        if len(v[i]) > len(v[index_max]):
            index_max = i
    return index_max

ranked_length = []

for i in range(len(temp_list)):
    ranked_length.append(temp_list.pop(find_index_longest(temp_list)))

j = 0
while j in range(len(ranked_length)):
    rank_length = len(ranked_length[j])
    print(f"Plats {j+1}:", end = "\n")
    while (j in range(len(ranked_length)) and len(ranked_length[j]) == rank_length):
        print(f"{ranked_length[j]}", end = "\n")
        j += 1
    print("\n")