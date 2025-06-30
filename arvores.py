import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as mpatches
import numpy as np
import random

NUM_TREES = 31
MAX_HEIGHT = 160
FPS = 30
LOOPS = 1

tree_types = ['cerejeira', 'laranjeira', 'palmeira', 'roseira', 'castanha', 'ipe']
colors_map = {
    'cerejeira': 'red',
    'laranjeira': 'orange',
    'palmeira': 'green',
    'roseira': 'pink',
    'castanha': 'brown',
    'ipe': 'purple'
}
growth_time_ranges = {
    'cerejeira': (9, 17),
    'laranjeira': (8, 15),
    'palmeira': (4, 9),
    'roseira': (5, 12),
    'castanha': (10, 18),
    'ipe': (4, 10)
}
final_height_ranges = {
    'cerejeira': (50, 70),
    'laranjeira': (40, 60),
    'palmeira': (90, 110),
    'roseira': (120, 140),
    'castanha': (120, 160),
    'ipe': (100, 130)
}

growth_phase_frames = FPS * 5
tractor_phase_frames = FPS * 5
cycle_frames = growth_phase_frames + tractor_phase_frames
total_frames = cycle_frames * LOOPS

wood_collected = {tt: 0 for tt in tree_types}


tree_types_per_tree = []
growth_times = []
final_heights = []
tree_colors = []
growth_rates = []

heights = np.zeros(NUM_TREES)
is_cut = np.zeros(NUM_TREES, dtype=bool)

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(range(NUM_TREES), heights, color='gray') 

legend_patches = [
    mpatches.Patch(color=color, label=tree) for tree, color in colors_map.items()
]
ax.legend(handles=legend_patches, title="Tipo de Árvore", loc='upper right', fontsize='small', title_fontsize='small')

tractor_height = 15
tractor_width = 3.5
tractor_rect = plt.Rectangle((-3, 0), tractor_width, tractor_height, color='yellow', visible=False)
ax.add_patch(tractor_rect)

ax.set_ylim(0, MAX_HEIGHT + 20)
ax.set_xlim(-1, NUM_TREES + 4)
ax.set_xlabel("Árvores")
ax.set_ylabel("Altura")
ax.set_title("Crescimento das Árvores e Trator Derrubando")

def setup_new_cycle():
    global tree_types_per_tree, growth_times, final_heights, tree_colors, growth_rates, heights, is_cut


    tree_types_per_tree = [random.choice(tree_types) for _ in range(NUM_TREES)]
    growth_times = [
        random.randint(*growth_time_ranges[tree_types_per_tree[i]]) for i in range(NUM_TREES)
    ]
    final_heights = np.array([
        random.uniform(*final_height_ranges[tree_types_per_tree[i]]) for i in range(NUM_TREES)
    ])

    #mais rápidas à esquerda
    sorted_indices = np.argsort(growth_times)
    tree_types_per_tree = [tree_types_per_tree[i] for i in sorted_indices]
    growth_times = [growth_times[i] for i in sorted_indices]
    final_heights = final_heights[sorted_indices]
    tree_colors = [colors_map[tt] for tt in tree_types_per_tree]

    growth_rates = [
        final_heights[i] / (growth_times[i] * FPS) for i in range(NUM_TREES)
    ]


    heights[:] = 0
    is_cut[:] = False

    #muda as cores
    for i, bar in enumerate(bars):
        bar.set_color(tree_colors[i])


setup_new_cycle()

def animate(frame):
    global heights, is_cut

    current_loop = frame // cycle_frames
    cycle_frame = frame % cycle_frames

    if cycle_frame == 0 and frame != 0:
        
        setup_new_cycle()

    if frame == total_frames - 1:
        #tabela
        print("\n---")
        print("## Madeira Coletada Pelo Trator")
        print("{:<12} {:>15}".format("espécie", "total de madeira"))
        print("-------------------------------")
        for tree_type, total in wood_collected.items():
            print("{:<12} {:>15.1f}".format(tree_type, total))
        plt.close()
        return []

    if cycle_frame < growth_phase_frames:
        tractor_rect.set_visible(False)
    else:
        tractor_rect.set_visible(True)
        tractor_progress = (cycle_frame - growth_phase_frames) / tractor_phase_frames
        tractor_x = tractor_progress * (NUM_TREES + 4) - 3
        tractor_rect.set_x(tractor_x)

        #trator derruba árvores
        for i in range(NUM_TREES):
            tree_center = i + 0.4
            if not is_cut[i] and tree_center <= (tractor_x + tractor_width):
                wood_collected[tree_types_per_tree[i]] += heights[i]
                heights[i] = 0
                is_cut[i] = True

    #arvores não cortadas continuam crescendo
    for i in range(NUM_TREES):
        if not is_cut[i] and heights[i] < final_heights[i]:
            heights[i] += growth_rates[i]
            if heights[i] > final_heights[i]:
                heights[i] = final_heights[i]
        bars[i].set_height(heights[i])

    return list(bars) + [tractor_rect]

ani = animation.FuncAnimation(
    fig, animate,
    frames=total_frames,
    interval=1000 / FPS,
    blit=False,
    repeat=False
)

plt.tight_layout()
plt.show()
