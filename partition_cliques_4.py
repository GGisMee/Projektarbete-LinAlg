import collections
import numpy as np

def remove_rows_and_columns(arr,index_arr):
    for i in reversed(range(np.shape(arr)[0])):
        if not i in index_arr:
            arr = np.delete(arr, i, 0)
            arr = np.delete(arr , i, 1)
    return arr

def BK(R,P,X,L,E):
    if len(P) == 0 and len(X) == 0:
        L.append(sorted(R))
        return
    for p in P.union(set([])):
        BK(R.union(set([p])),P.intersection(E[p]),X.intersection(E[p]),L,E)
        X.add(p)
        P.remove(p)

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
# behöver ändra tillbaka indexen i L1 så att de matchar ländernas index i den originella matrisem, annars tror jag koden funkar nu
def main():
    index = np.array([1,2,3])
    arr = np.array([[0,0,0,0,0,0,0],[0,0,1,1,0,0,0],[0,1,0,1,0,0,0],[0,1,1,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,1,1,0,0],[0,0,0,0,0,0,0]])
    L1 = []
    L2 = []
    arr = remove_rows_and_columns(arr,index)
    n = np.shape(arr)[0]
    for i in range(n):
        L2.append(i)
    BK(set([]),set(L2),set([]),L1,find_edges(arr))
    L1 = remove_sublist(L1)
    return L1

main()

