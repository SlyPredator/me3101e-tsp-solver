# 🗺️ Traveling Salesperson Problem (TSP) Solvers

This project solves and visualizes the Traveling Salesperson Problem using various MILP formulations. There are two solvers in it: one based on the Miller-Tucker-Zemlin (MTZ) formulation and one based on the Dantzig-Fulkerson-Johnson (DFJ) formulation. It also includes a data generation utility, which generates Euclidean distance matrices in a .csv file for a number of cities to be specified, and a tour plotter to visualize an animated solution. The main application lets the user choose the number of cities, automatically selects the appropriate solver depending on the problem size, and shows the optimal tour along with its cost and the execution time.

## 🚀 Key Features

* **Data Generation**: It generates the Euclidean distance matrices of instances for TSP.
* **MTZ Solver**: implements the MTZ formulation to solve TSP, which is appropriate for smaller problem sizes.
* **DFJ Solver**: implements the DFJ formulation with iterative subtour elimination and is therefore suitable for larger problem sizes.
* **Solver Selection**: Automatically selects the appropriate solver based on the number of cities.
* **Visualization**: Provides an animated plot of the optimal tour.
* **Performance Measurement**: Measures the execution time of the solvers and displays it.

## 🛠️ Tech Stack

*   **Programming Language**: Python
*   **MILP Solver**: PuLP
*   **Data Manipulation**: Pandas
*   **Numerical Computation**: NumPy
*   **Visualization**: Matplotlib (pyplot, animation)
*   **Data Storage**: Excel (using pandas)

## 📦 Getting Started

### Prerequisites

*   Python 3.12+

### Installation

1.  Clone the repository:

    ```bash
    git clone https://github.com/SlyPredator/me3101e-tsp-solver
    cd me3101e-tsp-solver
    ```

2.  Create a virtual environment (recommended):

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # On Linux/macOS
    .venv\Scripts\activate  # On Windows
    ```

3.  Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

### Running Locally

1.  Navigate to the project directory.
2.  Run the `main.py` script:

    ```bash
    python main.py
    ```

3.  The script will prompt you to enter the number of trips (locations). Enter a value between 10 and 100 (inclusive), in increments of 10.
4.  The script will then solve the TSP using the appropriate solver and display the results, including the optimal tour, total cost, and execution time. An animated plot of the tour will also be displayed.

## 📂 Project Structure

```
├── main.py
├── README.md
├── assets
│   └── dist_matrix.xlsx
│   └── demo.webm      
├── results              
│   └── trips_10.txt
│   └── trips_50.txt
│   └── trips_100.txt
├── solvers
│   ├── dfj_tsp.py
│   └── mtz_tsp.py
└── utils
    ├── generate_data.py
    └── trip_plotter.py
```

## 📸 Screenshots

A few verbose example results are present in the `results` folder so to as to see the outputs when `verbosity = 1` in `main.py`.

[demo.webm](https://github.com/user-attachments/assets/b39ebcbf-02c1-489d-bdac-9ea503b23b40)

