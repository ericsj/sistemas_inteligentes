import time

class Node:
    def __init__(self, board, g, previousNode):
        self.board = board
        self.previousNode = previousNode
        self.g = g
        self.h = self.get_h_socre()

    def get_h_socre(self):
        manhattan_value = 0

        def get_xy_by_coordinates(positionIn_puzzle_table):
            if positionIn_puzzle_table in [0, 3, 4]:
                x = -1
            elif positionIn_puzzle_table in [1, 4, 7]:
                x = 0
            else:
                x = 1

            if positionIn_puzzle_table in [0, 1, 2]:
                y = 1
            elif positionIn_puzzle_table in [3, 4, 5]:
                y = 0
            else:
                y = -1

            return x, y

        for position, number in enumerate(self.board):
            if number == None:
                current_number_position = get_xy_by_coordinates(position)
                right_number_position = get_xy_by_coordinates(8)
                manhattan_value += abs(current_number_position[0] - right_number_position[0]) + abs(current_number_position[1] - right_number_position[1])
            else:
                current_number_position = get_xy_by_coordinates(position)
                right_number_position = get_xy_by_coordinates(number - 1)
                manhattan_value += abs(current_number_position[0] - right_number_position[0]) + abs(current_number_position[1] - right_number_position[1])

        return manhattan_value

    def get_f_score(self):
        return self.g + self.h

    def is_equal(self, puzzle_node):
        return puzzle_node.to_string() == self.to_string()

    def to_string(self):
        return str(self.board)

    def get_path(self):
        if self.previousNode:
            return [self.previousNode.to_string()] + self.previousNode.get_path()
        return []

def is_finished(puzzle_node):
    finished_node = Node([1, 2, 3, 4, 5, 6, 7, 8, None], 0, None)
    return puzzle_node.is_equal(finished_node)

def get_actions_from_puzzle_node(puzzle_node):
    derived_nodes = []
    n_index_of_star = puzzle_node.board.index(None)
    if n_index_of_star in [0, 1, 2, 3, 4, 5]:
        derived_nodes.append(get_derived_puzzle_node_from_action(puzzle_node, 'down'))
    if n_index_of_star in [3, 4, 5, 6, 7, 8]:
        derived_nodes.append(get_derived_puzzle_node_from_action(puzzle_node, 'up'))
    if n_index_of_star in [0, 1, 3, 4, 6, 7]:
        derived_nodes.append(get_derived_puzzle_node_from_action(puzzle_node, 'right'))
    if n_index_of_star in [1, 2, 4, 5, 7, 8]:
        derived_nodes.append(get_derived_puzzle_node_from_action(puzzle_node, 'left'))
    return derived_nodes

def get_derived_puzzle_node_from_action(puzzle_node, action):
    n_index_of_star = puzzle_node.board.index(None)
    
    if action == 'up':
        derived_puzzle_node = puzzle_node.board[:]
        moved_piece = derived_puzzle_node[n_index_of_star - 3]
        derived_puzzle_node[n_index_of_star - 3] = None
        derived_puzzle_node[n_index_of_star] = moved_piece

        return Node(derived_puzzle_node, puzzle_node.g + 1, puzzle_node)

    if action == 'left':
        derived_puzzle_node = puzzle_node.board[:]
        moved_piece = derived_puzzle_node[n_index_of_star - 1]
        derived_puzzle_node[n_index_of_star - 1] = None
        derived_puzzle_node[n_index_of_star] = moved_piece

        return Node(derived_puzzle_node, puzzle_node.g + 1, puzzle_node)

    if action == 'right':
        derived_puzzle_node = puzzle_node.board[:]
        moved_piece = derived_puzzle_node[n_index_of_star + 1]
        derived_puzzle_node[n_index_of_star + 1] = None
        derived_puzzle_node[n_index_of_star] = moved_piece

        return Node(derived_puzzle_node, puzzle_node.g + 1, puzzle_node)

    if action == 'down':
        derived_puzzle_node = puzzle_node.board[:]
        moved_piece = derived_puzzle_node[n_index_of_star + 3]
        derived_puzzle_node[n_index_of_star + 3] = None
        derived_puzzle_node[n_index_of_star] = moved_piece

        return Node(derived_puzzle_node, puzzle_node.g + 1, puzzle_node)

def print_results(start_time, result_puzzle_node):
    end_time = time.time()
    result_path = result_puzzle_node.get_path()
    print('\nProblem solved. Stats:')
    print(f"Time taken: {end_time - start_time:.20f}")
    print('Number of visited nodes:',len(visited_puzzle_nodes))
    print('Path length:', len(result_path))
    print(f"path: {[p for p in result_path[::-1]]}")

def is_visited_node(puzzle_node):
    return any(visited_node.is_equal(puzzle_node) for visited_node in visited_puzzle_nodes)

visited_puzzle_nodes = []
border_puzzle_nodes = []

def a_star_manhattan_search(initial_value):
    start_time = time.time()
    result_puzzle_node = None

    initial_node = Node(initial_value, 0, None)
    print(f'\nSeu tabuleiro inicial é: {initial_node.to_string()}')

    if is_finished(initial_node):
        result_puzzle_node = initial_node
        print('O tabuleiro informado já é a solução final!')
        return print_results(start_time, result_puzzle_node)

    border_puzzle_nodes.append(initial_node)

    while border_puzzle_nodes:

        actual_puzzle_node = border_puzzle_nodes.pop(0)

        if is_finished(actual_puzzle_node):
            result_puzzle_node = actual_puzzle_node
            break

        visited_puzzle_nodes.append(actual_puzzle_node)
        derived_puzzle_nodes = get_actions_from_puzzle_node(actual_puzzle_node)

        for derived_puzzle_node in derived_puzzle_nodes:
            if is_visited_node(derived_puzzle_node):
                continue
            border_puzzle_nodes.append(derived_puzzle_node)
            border_puzzle_nodes.sort(key=lambda x: x.get_f_score())

    return print_results(start_time, result_puzzle_node)

