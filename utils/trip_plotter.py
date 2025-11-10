import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from sklearn.manifold import MDS
import warnings

warnings.filterwarnings("ignore", category=FutureWarning, module="sklearn")

def animated_plot_trip(distance_matrix, tour_order, title="TSP Optimal Tour"):
    n = len(distance_matrix)
    
    mds = MDS(n_components=2, dissimilarity='precomputed', random_state=42, normalized_stress='auto')
    coordinates = mds.fit_transform(distance_matrix)
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    ax.scatter(coordinates[:, 0], coordinates[:, 1], c='blue', s=200, alpha=0.8, zorder=3, edgecolors='black')
    
    for i, (x, y) in enumerate(coordinates):
        ax.annotate(str(i), (x, y), xytext=(10, 10), textcoords='offset points', fontsize=11, fontweight='bold', zorder=4,
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7))
    
    complete_tour = tour_order + [tour_order[0]]
    
    lines = []
    for i in range(len(complete_tour) - 1):
        start = complete_tour[i]
        end = complete_tour[i + 1]
        line, = ax.plot([coordinates[start, 0], coordinates[end, 0]], 
                       [coordinates[start, 1], coordinates[end, 1]], 
                       'gray', linewidth=2, alpha=0.4, zorder=1, linestyle='--')
        lines.append(line)
    
    arrow = ax.annotate('▶', xy=coordinates[complete_tour[0]], 
                       fontsize=24, zorder=5,
                       ha='center', va='center')
    
    info_box = ax.text(0.02, 0.98, '', transform=ax.transAxes, fontsize=12, verticalalignment='top', 
                      bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.9), fontweight='bold', zorder=6)
    
    total_cost = sum(distance_matrix[complete_tour[i]][complete_tour[i+1]] for i in range(len(complete_tour)-1))
    cost_box = ax.text(0.02, 0.88, f'Total Tour Cost: {total_cost:.2f}', transform=ax.transAxes, fontsize=11,
                      verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.9),
                      zorder=6)
    
    progress_box = ax.text(0.02, 0.82, '', transform=ax.transAxes, fontsize=10,
                          verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
                          zorder=6)
    
    def update(frame):
        total_segments = len(complete_tour) - 1
        frames_per_segment = 40
        total_frames = total_segments * frames_per_segment
        
        current_frame = frame % total_frames
        current_segment = current_frame // frames_per_segment
        t = (current_frame % frames_per_segment) / frames_per_segment
        
        for line in lines:
            line.set_color('gray')
            line.set_alpha(0.4)
            line.set_linestyle('--')
            line.set_linewidth(2)
        
        for i in range(current_segment):
            lines[i].set_color('green')
            lines[i].set_alpha(0.8)
            lines[i].set_linestyle('-')
            lines[i].set_linewidth(3)
        
        if current_segment < len(lines):
            lines[current_segment].set_color('blue')
            lines[current_segment].set_alpha(1.0)
            lines[current_segment].set_linestyle('-')
            lines[current_segment].set_linewidth(4)
        
        start_city = complete_tour[current_segment]
        end_city = complete_tour[current_segment + 1]
        distance = distance_matrix[start_city][end_city]
        
        info_box.set_text(f'Current Trip: {start_city} → {end_city}\nDistance: {distance:.2f}')
        progress = (current_segment + t) / total_segments * 100
        progress_box.set_text(f'Progress: {progress:.1f}%')
        start_coord = coordinates[start_city]
        end_coord = coordinates[end_city]
        
        x = start_coord[0] + t * (end_coord[0] - start_coord[0])
        y = start_coord[1] + t * (end_coord[1] - start_coord[1])
        
        arrow.set_position((x, y))
        dx = end_coord[0] - start_coord[0]
        dy = end_coord[1] - start_coord[1]
        angle = np.degrees(np.arctan2(dy, dx))
        arrow.set_rotation(angle)
        
        return [arrow, info_box, progress_box, cost_box] + lines
    
    total_segments = len(complete_tour) - 1
    ani = FuncAnimation(fig, update, frames=total_segments * 40, interval=40, blit=True, repeat=True, cache_frame_data=False)
    
    ax.set_title(f"{title}\nCity Layout", fontsize=14, fontweight='bold')
    ax.set_xlabel("X Coordinate")
    ax.set_ylabel("Y Coordinate")
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')
    
    plt.tight_layout()
    plt.show()