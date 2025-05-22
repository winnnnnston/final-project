import random

def random_shape(width, height, fill_prob=0.45, smooth_iters=3):
    """
    Generate a random cave-like map using cellular automata.

    Parameters:
      width (int):  number of columns
      height (int): number of rows
      fill_prob (float): initial probability of a wall cell
      smooth_iters (int): number of smoothing iterations

    Returns:
      List[List[str]]: 2D grid of '#' (wall) and '.' (open)
    """
    # Initialize with random noise
    grid = [['#' if random.random() < fill_prob else '.' for _ in range(width)]
            for _ in range(height)]

    # Smooth with cellular automata rules
    for _ in range(smooth_iters):
        new_grid = [row[:] for row in grid]
        for y in range(height):
            for x in range(width):
                walls = 0
                # Count walls in 8 neighbors (including out-of-bounds)
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        if dy == 0 and dx == 0:
                            continue
                        ny, nx = y + dy, x + dx
                        if not (0 <= ny < height and 0 <= nx < width):
                            walls += 1
                        elif grid[ny][nx] == '#':
                            walls += 1
                # Convert to wall if 5+ neighbors are walls
                new_grid[y][x] = '#' if walls >= 5 else '.'
        grid = new_grid
    return grid
