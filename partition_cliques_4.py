import collections
import numpy as np

def filter_out_cliques_with_2_or_less(cliques: list) -> list:
    filtered_cliques = []
    for clique in cliques:
        if len(clique) >= 3:
            filtered_cliques.append(clique)
    return filtered_cliques


def remove_rows_and_columns(arr,index_arr):
    '''Removes rows and columns which doesn't have indicies in index_arr'''
    for i in reversed(range(np.shape(arr)[0])):
        if not i in index_arr:
            arr = np.delete(arr, i, 0)
            arr = np.delete(arr , i, 1)
    return arr

#Modifierad Bron-Kerbosch algoritm, returnerar klickar och vissa delmängder av klickarna
def BK(R,P,X,L,E):
    '''Adds cliques to L (L1)'''
    if len(P) == 0 and len(X) == 0:
        L.append(sorted(R))
        return
    for p in P.union(set([])):
        BK(R.union(set([p])),P.intersection(E[p]),X.intersection(E[p]),L,E)
        X.add(p)
        P.remove(p)
#Sorterar bort delmängderna av klickarna så bara klickarna är kvar
def remove_sublist(lst):
    current = []
    result = []
    for element in sorted(map(set, lst), key = len, reverse = True):
        if not any(element <= req for req in current):
            current.append(element)
            result.append(list(element))     
    return result

def find_edges(matrix):
    n = np.shape(matrix)[0]
    edges = collections.defaultdict(set)
    for i in range(n):
        for j in range(n):
            if matrix[i,j] == 1:
                edges[i].add(j)
    return edges

#index ska vara index för alla länder i klickar och arr ska vara matrisen med 1 och 0 or
# behöver ändra tillbaka indexen i L1 så att de matchar ländernas index i den originella matrisen, annars tror jag koden funkar nu
def seperate_into_cliques(index:np.ndarray, arr:np.ndarray) -> list:
    '''Takes in some indicies and a directed matrix. Outputs which indices are in cliques with another.'''
    L1 = []
    arr = remove_rows_and_columns(arr,index)
    n = np.shape(arr)[0]
    L2 = list(range(n))
    BK(set([]),set(L2),set([]),L1,find_edges(arr))
    L1 = remove_sublist(L1)
    for i in range(len(L1)):
        for j in reversed(range(len(index))):
            L1[i] = [int(index[j]) if x == j else x for x in L1[i]]
    return L1

# Exempel från denna filen?
if __name__ == '__main__':
    index_1 = np.array([1,2,3])
    index_2 = np.array([1,2,3,4,5,7])
    input_arr1 = np.array([[0,0,0,0,0,0,0],[0,0,1,1,0,0,0],[0,1,0,1,0,0,0],[0,1,1,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,1,1,0,0],[0,0,0,0,0,0,0]])
    input_arr2 = np.array([[0,1,1,1,1,0,0,1,1],
                           [0,0,1,1,0,0,0,0,0], 
                           [1,1,0,1,0,0,0,0,0], 
                           [0,1,1,0,0,0,0,0,0], 
                           [1,0,0,0,0,1,1,1,0],
                           [1,0,0,0,1,0,1,1,0],
                           [0,0,0,0,1,1,0,1,0],
                           [1,1,1,0,0,1,1,0,0],
                           [1,1,1,0,1,1,0,0,0]])
    print(seperate_into_cliques(index_2, input_arr2))