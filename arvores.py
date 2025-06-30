import pygame
import random
import sys

# Configurações
NUM_TREES = 31
MAX_HEIGHT = 160
FPS = 30
LOOPS = 1

tree_types = ['cerejeira', 'laranjeira', 'palmeira', 'roseira', 'castanha', 'ipe']
colors_map = {
    'cerejeira': (255, 0, 0),
    'laranjeira': (255, 165, 0),
    'palmeira': (0, 128, 0),
    'roseira': (255, 105, 180),
    'castanha': (139, 69, 19),
    'ipe': (128, 0, 128)
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
tractor_phase_frames = FPS * 10
cycle_frames = growth_phase_frames + tractor_phase_frames
total_frames = cycle_frames * LOOPS

wood_collected = {tt: 0 for tt in tree_types}

# Inicialização do pygame
pygame.init()
screen_width = 1200
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Crescimento das Árvores e Trator Derrubando")
clock = pygame.time.Clock()

# Variáveis globais
tree_types_per_tree = []
growth_times = []
final_heights = []
tree_colors = []
growth_rates = []
heights = [0] * NUM_TREES
is_cut = [False] * NUM_TREES

# Trator
tractor_height = 30
tractor_width = 40
tractor_x = -tractor_width

# NOVO: carregar imagem do trator
tractor_img = pygame.image.load("trator.jpeg").convert_alpha()
tractor_img = pygame.transform.scale(tractor_img, (tractor_width, tractor_height))

# Dimensões
bar_width = screen_width // (NUM_TREES + 4)

def setup_new_cycle():
    global tree_types_per_tree, growth_times, final_heights, tree_colors, growth_rates, heights, is_cut
    tree_types_per_tree = [random.choice(tree_types) for _ in range(NUM_TREES)]
    growth_times = [
        random.randint(*growth_time_ranges[tree_types_per_tree[i]]) for i in range(NUM_TREES)
    ]
    final_heights = [
        random.uniform(*final_height_ranges[tree_types_per_tree[i]]) for i in range(NUM_TREES)
    ]
    # Ordenar por crescimento mais rápido à esquerda
    sorted_indices = sorted(range(NUM_TREES), key=lambda i: growth_times[i])
    tree_types_per_tree = [tree_types_per_tree[i] for i in sorted_indices]
    growth_times = [growth_times[i] for i in sorted_indices]
    final_heights = [final_heights[i] for i in sorted_indices]
    tree_colors = [colors_map[tt] for tt in tree_types_per_tree]
    growth_rates = [
        final_heights[i] / (growth_times[i] * FPS) for i in range(NUM_TREES)
    ]
    heights[:] = [0] * NUM_TREES
    is_cut[:] = [False] * NUM_TREES

setup_new_cycle()

frame = 0
running = True

while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()

    screen.fill((240, 240, 240))  # fundo claro

    current_loop = frame // cycle_frames
    cycle_frame = frame % cycle_frames

    if cycle_frame == 0 and frame != 0:
        setup_new_cycle()

    if frame >= total_frames:
        print("\n---")
        print("## Madeira Coletada Pelo Trator")
        print("{:<12} {:>15}".format("espécie", "total de madeira"))
        print("-------------------------------")
        for tree_type, total in wood_collected.items():
            print("{:<12} {:>15.1f}".format(tree_type, total))
        pygame.time.wait(2000)
        running = False
        continue

    if cycle_frame < growth_phase_frames:
        tractor_visible = False
    else:
        tractor_visible = True
        tractor_progress = (cycle_frame - growth_phase_frames) / tractor_phase_frames
        tractor_x = int(tractor_progress * (screen_width + tractor_width)) - tractor_width

        # Trator corta árvores
        for i in range(NUM_TREES):
            tree_left = i * bar_width + bar_width // 2
            if not is_cut[i] and (tree_left + bar_width//2) <= (tractor_x + tractor_width):
                wood_collected[tree_types_per_tree[i]] += heights[i]
                heights[i] = 0
                is_cut[i] = True

    # Crescimento das árvores
    for i in range(NUM_TREES):
        if not is_cut[i] and heights[i] < final_heights[i]:
            heights[i] += growth_rates[i]
            if heights[i] > final_heights[i]:
                heights[i] = final_heights[i]
        # Desenhar árvore
        h = int((heights[i] / MAX_HEIGHT) * (screen_height - 50))
        tree_x = i * bar_width + bar_width // 2
        tree_y = screen_height - h
        pygame.draw.rect(screen, tree_colors[i], (tree_x, tree_y, bar_width // 2, h))

    # NOVO: desenhar o trator como imagem
    if tractor_visible:
        screen.blit(tractor_img, (tractor_x, screen_height - tractor_height))

    pygame.display.flip()
    frame += 1

pygame.quit()
