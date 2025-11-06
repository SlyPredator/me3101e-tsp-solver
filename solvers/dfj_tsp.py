import pulp
import pandas as pd


class DFJ_Solver():
    def __init__(self):
        pass
    
    def load_dists(self, file_path, sheet_name):
        df = pd.read_excel(file_path, sheet_name=sheet_name, header=None, index_col=None)
        dist_mat = df.to_numpy()
        return dist_mat

    def solve_tsp_dfj(self, dist_mat, verbose, time_limit=300):
        n = len(dist_mat)
        problem = pulp.LpProblem("DFJ_TSP_Solver", pulp.LpMinimize)
        x = [[pulp.LpVariable(f"x_{i}_{j}", cat="Binary") for j in range(n)] for i in range(n)]
        problem += pulp.lpSum(dist_mat[i][j] * x[i][j] for i in range(n) for j in range(n) if i != j)

        for i in range(n):
            problem += pulp.lpSum(x[i][j] for j in range(n) if i != j) == 1, f"out_degree_{i}"
        
        for j in range(n):
            problem += pulp.lpSum(x[i][j] for i in range(n) if i != j) == 1, f"in_degree_{j}"

        problem.solve(pulp.PULP_CBC_CMD(msg=verbose, timeLimit=time_limit))
        
        if pulp.LpStatus[problem.status] != "Optimal":
            return {"status": pulp.LpStatus[problem.status]}

        def internal_loops(x_vals, n):
            visited = [False] * n
            subtrips = []
            
            for i in range(n):
                if not visited[i]:
                    current = i
                    subtrip = []
                    while not visited[current]:
                        visited[current] = True
                        subtrip.append(current)
                        for j in range(n):
                            if current != j and x_vals[current][j] > 0.5:
                                current = j
                                break
                    if len(subtrip) > 1:
                        subtrips.append(subtrip)
            
            return subtrips
        
        max_iters = 100
        for iteration in range(max_iters):
            x_vals = [[pulp.value(x[i][j]) for j in range(n)] for i in range(n)]
            subtrips = internal_loops(x_vals, n)
            if len(subtrips) <= 1:
                break
            
            print(f"Iteration {iteration + 1}: Found {len(subtrips)} subtrips")
            for subtrip in subtrips:
                if len(subtrip) < n:
                    problem += (pulp.lpSum(x[i][j] for i in subtrip for j in subtrip if i != j) <= len(subtrip) - 1,
                        f"subtrip_elim_{iteration}_{subtrip[0]}")

            problem.solve(pulp.PULP_CBC_CMD(msg=verbose, timeLimit=time_limit))
            
            if pulp.LpStatus[problem.status] != "Optimal":
                break

        if pulp.LpStatus[problem.status] == "Optimal":
            total_cost = pulp.value(problem.objective)

            trip_edges = []
            for i in range(n):
                for j in range(n):
                    if i != j and pulp.value(x[i][j]) > 0.5:
                        trip_edges.append((i, j))

            trip_order = []
            if trip_edges:
                current = 0
                visited = set()
                while len(trip_order) < n:
                    trip_order.append(current)
                    visited.add(current)
                    for j in range(n):
                        if current != j and pulp.value(x[current][j]) > 0.5 and j not in visited:
                            current = j
                            break
            
            return {
                "trip_edges": trip_edges,
                "trip_order": trip_order,
                "total_cost": total_cost,
                "iterations": iteration + 1
            }
        else:
            return {"status": pulp.LpStatus[problem.status]}