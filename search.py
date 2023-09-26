import heapq
from pacUtility import GRID


# Define possible movements (up, down, left, right)
movements = [(1, 0), (-1, 0), (0, 1), (0, -1)]

def dijkstra(start, end):
    rows, cols = len(GRID), len(GRID[0])

    # Helper function to check if a cell is valid and not visited
    def is_valid(y, x):
        return 0 <= y < rows and 0 <= x < cols and GRID[y][x] == 1

    # Initialize distance dictionary and priority queue
    distance = {(i, j): float('inf') for i in range(rows) for j in range(cols)}
    distance[start] = 0
    priority_queue = [(0, start)]  # (distance, node)

    # Initialize predecessor dictionary
    predecessor = {}

    while priority_queue:
        dist, current = heapq.heappop(priority_queue)

        if current == end:
            break

        for dx, dy in movements:
            y, x = current[0] + dx, current[1] + dy

            if is_valid(y, x):
                new_distance = dist + 1  # Assuming each move has a cost of 1

                if new_distance < distance[(y, x)]:
                    distance[(y, x)] = new_distance
                    heapq.heappush(priority_queue, (new_distance, (y, x)))
                    predecessor[(y, x)] = current

    # Reconstruct the path
    path = []
    current = end
    while current != start:
        path.append(current)
        current = predecessor[current]
    path.append(start)
    path.reverse()

    return path



def heuristic(node, goal):
    # Manhattan distance heuristic
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

def aStar(start, end):
    rows, cols = len(GRID), len(GRID[0])
    open_list = []
    closed_set = set()
    came_from = {}

    g_score = {node: float('inf') for row in GRID for node in row}
    f_score = {node: float('inf') for row in GRID for node in row}
    
    g_score[start] = 0
    f_score[start] = heuristic(start, end)

    heapq.heappush(open_list, (f_score[start], start))

    while open_list:
        _, current = heapq.heappop(open_list)

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        closed_set.add(current)

        for dr, dc in movements:
            neighbor = (current[0] + dr, current[1] + dc)

            if (
                0 <= neighbor[0] < rows
                and 0 <= neighbor[1] < cols
                and GRID[neighbor[0]][neighbor[1]] == 1
            ):
                tentative_g_score = g_score[current] + 1

                if tentative_g_score < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)

                    if neighbor not in closed_set:
                        heapq.heappush(open_list, (f_score[neighbor], neighbor))

    return None  # No path found