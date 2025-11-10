import pulp
import pandas as pd


class MTZ_Solver():
    def _init__(self):
        pass

    def load_dists(self, file_path, sheet):
        df = pd.read_excel(file_path, sheet_name=sheet, header=None, index_col=None)
        dist_mat = df.to_numpy()
        return dist_mat

    def solve_tsp_mtz(self, dist_mat, verbosity):
        n = len(dist_mat)
        problem = pulp.LpProblem("MTZ_TSP_Solver", pulp.LpMinimize)
        x = [[pulp.LpVariable(f"x_{i}_{j}", cat="Binary") for j in range(n)] for i in range(n)]
        u = [pulp.LpVariable(f"u_{i}", lowBound=0, upBound=n-1, cat="Continuous") for i in range(n)]
        problem += pulp.lpSum(dist_mat[i][j] * x[i][j] for i in range(n) for j in range(n) if i != j)
        for j in range(n):
            problem += pulp.lpSum(x[i][j] for i in range(n) if i != j) == 1
        
        for i in range(n):
            problem += pulp.lpSum(x[i][j] for j in range(n) if i != j) == 1
        
        for i in range(1, n):
            for j in range(1, n):
                if i != j:
                    problem += u[i] - u[j] + (n - 1) * x[i][j] <= n - 2

        problem.solve(pulp.PULP_CBC_CMD(msg=verbosity))

        trip = []
        if pulp.LpStatus[problem.status] == "Optimal":
            total_cost = pulp.value(problem.objective)
            for i in range(n):
                for j in range(n):
                    if pulp.value(x[i][j]) == 1:
                        trip.append((i, j))
            return {"trip": trip, "total_cost": total_cost}
        else:
            return {"status": pulp.LpStatus[problem.status]}
