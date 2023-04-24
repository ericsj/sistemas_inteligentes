import sys
import time
import copy

ordered_board = [1,2,3,4,5,6,7,8,None]


class Node:
  def __init__(self, board, previous_node, distance_from_source):
    self.board = board
    self.previous_node = previous_node
    self.distance_from_source = distance_from_source

  def get_path(self):
    result = [self.board]
    if self.previous_node:
      result.append(self.previous_node.get_path())
      return result
    return self.board

def check_game_over(node):
  return node.board == ordered_board

def print_stats(start_time, target_node, visited_nodes):
  time_taken = time.time() - start_time
  print('Problem solved. Stats:')
  print('Number of visited nodes:', visited_nodes)
  path = target_node.get_path()
  print('Path length:', len(path))
  print('Time taken: ', time_taken)

def get_state_after_move_space_down(node):
  empty_index = node.board.index(None)
  derived_node = copy.deepcopy(node.board)
  moved_number = derived_node[empty_index + 3]
  derived_node[empty_index + 3] = None
  derived_node[empty_index] = moved_number
  return Node(derived_node, node, node.distance_from_source + 1)

def get_state_after_move_space_up(node):
  empty_index = node.board.index(None)
  derived_node = copy.deepcopy(node.board)
  moved_number = derived_node[empty_index - 3]
  derived_node[empty_index - 3] = None
  derived_node[empty_index] = moved_number
  return Node(derived_node, node, node.distance_from_source + 1)

def get_state_after_move_space_right(node):
  empty_index = node.board.index(None)
  derived_node = copy.deepcopy(node.board)
  moved_number = derived_node[empty_index + 1]
  derived_node[empty_index + 1] = None
  derived_node[empty_index] = moved_number
  return Node(derived_node, node, node.distance_from_source + 1)
 
def get_state_after_move_space_left(node):
  empty_index = node.board.index(None)
  derived_node = copy.deepcopy(node.board)
  moved_number = derived_node[empty_index - 1]
  derived_node[empty_index - 1] = None
  derived_node[empty_index] = moved_number
  return Node(derived_node, node, node.distance_from_source + 1)

def get_derived_nodes(node):
  derived_nodes = []
  empty_index = node.board.index(None)
  uppermost_slice_indexes = [0,1,2,3,4,5]
  bottommost_slice_indexes = [3,4,5,6,7,8]
  leftmost_slice_indexes = [0,1,3,4,6,7]
  rightmost_slice_indexes = [1,2,4,5,7,8]
  if empty_index in uppermost_slice_indexes:
    derived_nodes.append(get_state_after_move_space_down(node))
  if empty_index in bottommost_slice_indexes:
    derived_nodes.append(get_state_after_move_space_up(node))
  if empty_index in leftmost_slice_indexes:
    derived_nodes.append(get_state_after_move_space_right(node))
  if empty_index in rightmost_slice_indexes:
    derived_nodes.append(get_state_after_move_space_left(node))
  return derived_nodes

def uniform_cost_search(initial_board):
  start_time = time.time()
  initial_node = Node(initial_board, None, 0)
  visited_nodes = []
  visited_nodes_number = 1
  priority_queue = []
  target_node = None
  priority_queue.append(initial_node)
  while(len(priority_queue)):
    picked_node = priority_queue.pop(0)
    if check_game_over(picked_node):
      target_node = picked_node
      print_stats(start_time, target_node, visited_nodes_number)
      return
    visited_nodes.append(picked_node)
    derived_nodes = get_derived_nodes(picked_node)
    for derived_node in derived_nodes:
      if derived_node not in visited_nodes:
        priority_queue.append(derived_node)
        priority_queue.sort(key=lambda x: x.distance_from_source)
        visited_nodes_number+=1

  print('Problem not solved, please check if your input is valid')
