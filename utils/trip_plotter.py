import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

def animated_plot_tour(distance_matrix, tour_order, title="TSP Optimal Tour"):
    n = len(distance_matrix)

    angles = np.linspace(0, 2*np.pi, n, endpoint=False)
    coordinates = np.column_stack([np.cos(angles), np.sin(angles)])
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    ax.scatter(coordinates[:, 0], coordinates[:, 1], c='blue', s=150, alpha=0.7, zorder=3)
    
    for i, (x, y) in enumerate(coordinates):
        ax.annotate(str(i), (x, y), xytext=(8, 8), textcoords='offset points', 
                    fontsize=12, fontweight='bold', zorder=4)
    
    complete_tour = tour_order + [tour_order[0]]

    lines = []
    for i in range(len(complete_tour) - 1):
        start = complete_tour[i]
        end = complete_tour[i + 1]
        line, = ax.plot([coordinates[start, 0], coordinates[end, 0]], 
                       [coordinates[start, 1], coordinates[end, 1]], 
                       'r-', linewidth=2, alpha=0.7, zorder=1)
        lines.append(line)
    
    arrow = ax.annotate('➤', xy=coordinates[complete_tour[0]], 
                       fontsize=20, color='green', zorder=5,
                       ha='center', va='center')
    text_box = ax.text(0.02, 0.98, '', transform=ax.transAxes, fontsize=12,
                      verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
                      fontweight='bold', zorder=6)
    
    def update(frame):
        total_segments = len(complete_tour) - 1
        frames_per_segment = 30
        total_frames = total_segments * frames_per_segment
        
        current_frame = frame % total_frames
        current_segment = current_frame // frames_per_segment
        t = (current_frame % frames_per_segment) / frames_per_segment

        for line in lines:
            line.set_color('r')
        
        if current_segment < len(lines):
            lines[current_segment].set_color('b')
        
        start_city = complete_tour[current_segment]
        end_city = complete_tour[current_segment + 1]

        distance = distance_matrix[start_city][end_city]
        text_box.set_text(f'From: {start_city} → To: {end_city}\nDistance: {distance:.2f}')
        
        start_coord = coordinates[start_city]
        end_coord = coordinates[end_city]

        x = start_coord[0] + t * (end_coord[0] - start_coord[0])
        y = start_coord[1] + t * (end_coord[1] - start_coord[1])

        arrow.set_position((x, y))

        dx = end_coord[0] - start_coord[0]
        dy = end_coord[1] - start_coord[1]
        angle = np.degrees(np.arctan2(dy, dx))
        arrow.set_rotation(angle)
        
        return [arrow, text_box] + lines

    total_segments = len(complete_tour) - 1
    ani = FuncAnimation(fig, update, frames=total_segments * 30, 
                       interval=50, blit=True, repeat=True, cache_frame_data=False)
    
    ax.set_title(f"{title}\nTotal Cities: {n}", fontsize=14)
    ax.axis('equal')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()