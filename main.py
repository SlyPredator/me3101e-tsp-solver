from time import time

from solvers.mtz_tsp import MTZ_Solver
from solvers.dfj_tsp import DFJ_Solver
from utils.trip_plotter import animated_plot_tour

mtz = MTZ_Solver()
dfj = DFJ_Solver()

verbose = 0

file_path = r"assets/dist_matrix.xlsx"
print("Welcome to our Operations Research Project - Delivery Optimization using TSP!\n")
trip_count = input("Enter the number of trips (10, 20, 30, ... ,100): ")

try:
    if int(trip_count) < 30:
        dist_mat = mtz.load_dists(file_path, "trips_" + trip_count)
        print(f"\nUsing Miller-Tucker-Zemlin Approach..\n")

        start_time = time()
        result = mtz.solve_tsp_mtz(dist_mat, verbose)
        end_time = time()

        edges = {fr: to for fr, to in result["trip"]}
        trip_open = [0]
        current = 0
        
        for _ in range(len(dist_mat) - 1):
            current = edges.get(current)
            if current is None:
                print("ERROR: Tour is broken, check solver constraints.")
                break
            trip_open.append(current)
        
        trip_closed = trip_open + [0]
        
        print(f"Optimal Trip Order: {" -> ".join(str(x) for x in trip_closed)}")
        print(f"Total Cost: {result['total_cost']:.3f}")
        print(f"Time taken to solve the problem: {end_time - start_time:.3f} seconds")
        animated_plot_tour(dist_mat, trip_open, f"MTZ Solution - {trip_count} Trips")
        
    else:
        print(f"\nCan't solve for {trip_count} trips using Miller-Tucker-Zemlin Approach quickly enough..")
        dist_mat = dfj.load_dists(file_path, "trips_" + trip_count)
        print(f"\nUsing Dantzig-Fulkerson-Johnson Approach..\n")

        start_time = time()
        result = dfj.solve_tsp_dfj(dist_mat, verbose, time_limit=600)
        end_time = time()

        trip_open = result['trip_order']
        trip_closed = trip_open + [0]

        print(f"\nOptimal Trip Order: {" -> ".join(str(x) for x in trip_closed)}")
        print(f"Total Objective Cost: {result['total_cost']:.3f}")
        print(f"Time taken to solve the problem: {end_time - start_time:.3f} seconds")

        animated_plot_tour(dist_mat, trip_open, f"DFJ Solution - {trip_count} Trips")

except ValueError:
    print("\nEnter a multiple of 10 from 10-100!")