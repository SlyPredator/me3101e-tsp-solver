import pandas as pd
import numpy as np

def euclidian_distances(n_cities, area_size=100, seed=None):
    if seed:
        np.random.seed(seed)
    
    coords = np.random.rand(n_cities, 2) * area_size
    dist_matrix = np.zeros((n_cities, n_cities))
    
    for i in range(n_cities):
        diffs = coords - coords[i]
        dist_matrix[i] = np.sqrt(np.sum(diffs**2, axis=1))
    
    return dist_matrix

with pd.ExcelWriter(r"../assets/dist_matrix.xlsx", engine='openpyxl') as writer:
    for n in [10,20,30,40,50,60,70,80,90,100]:
        pd.DataFrame(euclidian_distances(n)).to_excel(
            writer, sheet_name=f"trips_{n}", index=False, header=False)
        print(f"Made dataset for trips_{n}..")
    print("Done generating the data matrices for required number of trips!")