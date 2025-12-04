#from partition_cliques_4.py import list

def find_index_longest(v):
    #Hittar index för längsta listan i lista v, returnerar index
    index_max = 0
    for i in range(len(v)):
        if len(v[i]) > len(v[index_max]):
            index_max = i
    return index_max

def print_result(ranked_by_length):
    '''Prints lists in order'''
    j = 0
    while j in range(len(ranked_by_length)):
        rank_length = len(ranked_by_length[j])
        print(f"Plats {j+1}:", end = "\n")
        while (j in range(len(ranked_by_length)) and len(ranked_by_length[j]) == rank_length):
            print(f"{ranked_by_length[j]}", end = "\n")
            j += 1
        print()

def rank(temp_list:list):
    '''Rankar vilken som är längst'''
    ranked_by_length = []
    for i in range(len(temp_list)):
        ranked_by_length.append(temp_list.pop(find_index_longest(temp_list)))
    print_result(ranked_by_length)

if __name__ == "__main__":
    #Lista för att testa
    a = [1, 2, 3]
    b = [0, 1, 2]
    c = [4]
    d = [3, 5, 6, 9]
    temp_list = [a, b, c, d]
    rank(temp_list)