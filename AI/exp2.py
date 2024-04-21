import heapq

class State:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.parent = None
        self.cost = 0
        self.heuristic = 0

    def __lt__(self, other):
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)

def is_goal(state, target_x, target_y):
    return state.x == target_x and state.y == target_y

def get_successors(state, capacity_x, capacity_y):
    successors = []
    
    successors.append(State(capacity_x, state.y))
    
    successors.append(State(state.x, capacity_y))
    
    successors.append(State(0, state.y))
    
    successors.append(State(state.x, 0))
    
    pour_amount = min(state.x, capacity_y - state.y)
    successors.append(State(state.x - pour_amount, state.y + pour_amount))
    
    pour_amount = min(state.y, capacity_x - state.x)
    successors.append(State(state.x + pour_amount, state.y - pour_amount))
    
    return successors

def heuristic(state, target_x, target_y):
    return abs(state.x - target_x) + abs(state.y - target_y)

def a_star(start_x, start_y, target_x, target_y, capacity_x, capacity_y):
    start_state = State(start_x, start_y)
    start_state.heuristic = heuristic(start_state, target_x, target_y)
    
    open_list = []
    closed_list = set()
    
    heapq.heappush(open_list, start_state)
    
    while open_list:
        current_state = heapq.heappop(open_list)
        
        if is_goal(current_state, target_x, target_y):
            path = []
            while current_state:
                path.insert(0, (current_state.x, current_state.y))
                current_state = current_state.parent
            return path
        
        closed_list.add((current_state.x, current_state.y))
        
        for successor in get_successors(current_state, capacity_x, capacity_y):
            successor.cost = current_state.cost + 1
            successor.heuristic = heuristic(successor, target_x, target_y)
            
            if (successor.x, successor.y) in closed_list:
                continue
            
            if successor not in open_list:
                successor.parent = current_state
                heapq.heappush(open_list, successor)
    
    return None

start_x = 0
start_y = 0
target_x = 4
target_y = 0
capacity_x = 5
capacity_y = 3

path = a_star(start_x, start_y, target_x, target_y, capacity_x, capacity_y)
print(path)
