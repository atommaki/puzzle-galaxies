#!/usr/bin/env python3

import copy

class bcolors:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    GRAY = '\033[90m'
    RED2 = '\033[91m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

    COLORS=[ RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, GRAY ]


class galaxy_field:

  def __init__(self,n,centers, board=None):
    self.centers = centers
    self.board_size = n
    if board == None:
        self.board = []
    else:
        self.board = copy.deepcopy(board)
    self.difficulty = None
    self.nsolutions = None
    for i in range(n):
      self.board.append([])
      for j in range(n):
        self.board[i].append(None)
    self.sanity_check()

  def sanity_check(self):
    self.centers_sanity_check()

  def centers_sanity_check(self):
    if len(self.centers) < 1:
      raise ValueError('Gravity center list is empty')
    for cx, cy in self.centers:
      if not self.is_on_board(cx,cy):
        raise ValueError(f'Gravity center is out of the board: {cx},{cy} (board_size={self.board_size})')

  def solve(self):
    self.solve_phase_1() or self.solve_phase_2()

    if self.is_solved(): return True

    while self.solve_phase_3():
        self.solve_phase_2()

    if self.is_solved(): return True

    self.solve_phase_3(try_hard=True)


  def solve_phase_1(self):
    # mark tiles which are directly touching a galaxy center
    for i in range(self.board_size):
      for j in range(self.board_size):
        if self.board[i][j] == None:
          c = self.get_center_in_touch(j,i)
          self.board[i][j] = c
    self.difficulty = 0
    return self.is_solved()

  def solve_phase_2(self):
    # mark tiles where only one galaxy center is possible (reachable + mirror point is free)
    change = True
    any_change = False
    while change:
      change = False
      self.difficulty += 1
      for i in range(self.board_size):
        for j in range(self.board_size):
          if self.board[i][j] != None:
            continue
          reachable = self.get_reachable_centers(j,i)
          possible = self.get_possible_centers(j,i)
          reachable_and_possible = reachable & possible
          #print(f'x={j=}  y={i=}  {reachable_and_possible=}  {reachable=}  {possible=}')
          if len(reachable_and_possible) == 1:
            c = reachable_and_possible.pop()
            self.mark_point_and_mirror_point(j,i, c)
            change = True
            any_change = True
    return any_change

  def solve_phase_3(self,try_hard=False):
    # connect separated parts of a galaxy (if there is any)
    change = True
    any_change = False
    while change:
      change = False
      for i in range(self.board_size):
        for j in range(self.board_size):
          if self.board[i][j] == None:
            continue
          if not self.is_connected_galaxy(j,i,self.board[i][j]):
            if self.try_to_connect_galaxy(j,i,self.board[i][j], try_hard=try_hard):
              change = True
              any_change = True
    return any_change

  def solve_phase_4(self):
    pass

  def get_neighbors(self,x,y):
    neighbors=set()
    check_list = { (x+1, y), (x-1, y), (x, y+1), (x, y-1) }
    for xx, yy in check_list:
      if self.is_on_board(xx, yy):
        neighbors.add((xx,yy))
    return neighbors

  def is_connected_galaxy(self, x,y,c, already_checked=set()):
    if self.get_center_in_touch(x,y) == c:
      return True
    neighbors = self.get_neighbors(x,y)
    already_checked_new = already_checked | { (x,y) } | neighbors
    for xx, yy in neighbors:
      if (xx,yy) not in already_checked and self.board[yy][xx] == self.board[y][x]:
        if self.is_connected_galaxy(xx,yy,c, already_checked = already_checked_new):
          return True
    return False

  def try_to_connect_galaxy(self, x,y,c, try_hard=False):
    neighbors = self.get_neighbors(x,y)
    good_neighbors = set()
    any_change = False
    for xx, yy in neighbors:
      if self.board[yy][xx] == None and c in self.get_reachable_centers(xx,yy):
        good_neighbors.add((xx,yy))
    if len(good_neighbors) == 1:
      self.difficulty += 100
      xx, yy = good_neighbors.pop()
      self.mark_point_and_mirror_point(xx, yy, c)
      any_change = True
      if not self.is_connected_galaxy(xx,yy,c):
        self.try_to_connect_galaxy(xx,yy,c)
    elif try_hard:
      self.difficulty += 10000
      possible_solutions = set()
      for xx, yy in good_neighbors:
        bb = galaxy_field(self.board_size, self.centers, self.board)
        bb.mark_point_and_mirror_point(xx,yy,c)
        bb.solve()
        if bb.is_solved():
          possible_solutions.add((xx,yy))
      if len(possible_solutions) > 0:
        xx, yy = possible_solutions.pop()
        self.mark_point_and_mirror_point(xx,yy,c)
        self.solve()
    return any_change

  def mark_point_and_mirror_point(self, x,y, c):
    self.board[y][x] = c
    mx, my = self.get_mirror_point(x,y, c[0], c[1])
    self.board[my][mx] = c

  def is_on_board(self, x, y):
    if x < 0 or x >= self.board_size or y < 0 or y >= self.board_size:
      return False
    return True

  def get_center_in_touch(self,x,y):
     for c in [ (x,y), (x+0.5, y), (x-0.5,y), (x, y+0.5), (x,y-0.5),
                (x+0.5, y+0.5), (x+0.5,y-0.5), (x-0.5, y+0.5), (x-0.5, y-0.5) ]:
       if c in self.centers:
         return c
     return None

  def is_solved(self):
    for i in range(self.board_size):
      for j in range(self.board_size):
        if self.board[i][j] == None:
          return False
    return True

  def get_reachable_centers(self, x,y, already_checked=set()):
    if self.board[y][x] != None:
      return { self.board[y][x] }
    reachable = set()
    neighbors = self.get_neighbors(x,y)
    already_checked_new = already_checked | { (x,y) } | neighbors
    for xx, yy in neighbors:
      if (xx,yy) in already_checked:
         continue
      reachable = reachable | self.get_reachable_centers(xx, yy, already_checked = already_checked_new)
    return reachable

  def get_mirror_point(self, x,y, cx, cy):
    return int(cx-(x-cx)), int(cy-(y-cy))

  def get_possible_centers(self, x,y):
    possible = set()
    for cx, cy in self.centers:
      mx, my = self.get_mirror_point(x,y,cx,cy)
      if self.is_on_board(mx,my) and self.board[my][mx] == None:
        possible.add((cx,cy))
    return possible

  def is_center(self, x, y):
    if (x,y) in self.centers:
      return True
    else:
      return False

  def get_color(self, c):
    return bcolors.COLORS[self.centers.index(c) % len(bcolors.COLORS)]

  def is_horizontal_border(self, x,y):
    if x != int(x):
      return self.is_horizontal_border(x-0.5, y) or self.is_horizontal_border(x+0.5, y) or self.is_vertical_border(x, y-0.5) or self.is_vertical_border(x, y+0.5)
    x = int(x)
    if not self.is_on_board(x,y-0.5) or not self.is_on_board(x,y+0.5):
      return True
    if self.board[int(y-0.5)][x] == None or self.board[int(y+0.5)][x] == None:
      return False
    if self.board[int(y-0.5)][x] != self.board[int(y+0.5)][x]:
      return True
    return False

  def is_vertical_border(self, x,y):
    if y != int(y):
      return False
      return self.is_vertical_border(x, y-0.5) or self.is_vertical_border(x, y+0.5)
    y = int(y)
    if not self.is_on_board(x-0.5,y) or not self.is_on_board(x+0.5,y):
      return True
    if self.board[y][int(x-0.5)] == None or self.board[y][int(x+0.5)] == None:
      return False
    if self.board[y][int(x-0.5)] != self.board[y][int(x+0.5)]:
      return True
    return False

  def show(self, showgrid=True, showborder=False, showunknown=False):
    for i in range(-1, self.board_size*2):
      for j in range(-1, self.board_size*2):
        if self.is_center(j/2,i/2):
          print(f'{self.get_color((j/2,i/2))}o{bcolors.RESET} ', end='')
        else:
          sign = '  '
          if showgrid or showborder and (self.is_horizontal_border(j/2,i/2) or self.is_vertical_border(j/2,i/2)):
              if i/2 != i//2 and j/2 != j//2:
                sign = '+ '
              elif i/2 != i//2:
                sign = '- '
              elif j/2 != j//2 and (showgrid or showborder and self.is_vertical_border(j/2,i/2)):
                sign = '| '

          if i/2 == i//2 and j/2 == j//2:
            if not showborder and j//2 < self.board_size and i//2 < self.board_size and i >= 0 and j >=0 and self.board[i//2][j//2] != None:
              sign = f'{self.get_color(self.board[i//2][j//2])}x{bcolors.RESET} '
            elif showunknown and self.board[i//2][j//2] == None:
              sign = '? '

          print(sign, end='')

      print()
    print()
#    print(self.board)



# 5x5 normal, ID = 1_758_394
#b = galaxy_field(5,[(0.5,0), (3.5,0), (2.5,1), (0.5, 2.5), (4, 2.5), (2,3), (3,3.5)])

# 7x7 hard, ID = 3_240_019
#b = galaxy_field(7, [(1.5,0), (4,0), (0,1), (2.5, 1.5), (5,2.5), (3.5, 3.5), (6, 3.5), (1.5, 4.5), (0, 5.5), (1,6), (4.5,6)])

# 7x7 hard, ID = 2_243_248
#b = galaxy_field(7, [(2,0), (4,0.5), (0,1), (5.5,1.5), (2.5,2), (2.5,3), (2.5,4), (6,4), (0,4.5), (1,5), (5,5), (6,5.5), (2.5,6)])

# 7x7 hard, ID = 381_831
b = galaxy_field(7, [(1.5,0.5), (4.5,0.5), (6,0.5), (1,2), (3,2.5), (0,3), (5,3), (1,3.5), (4,4), (0.5,5), (3,5), (5,5), (0,6), (5.5,6)])

# 10x10 hard, ID = 2_851_686
#b = galaxy_field(10, [(5,0.5), (3.5,1), (7,1), (0,1.5), (1.5,2.5), (4,2.5), (7.5,3), (9,3), (0,4), (5,4), (3,5), (8,5), (0.5,7), (4,7), (7,7), (2,7.5), (6,8), (8.5,8), (4,8.5), (0.5,9), (3,9)])

# 15x15 hard, ID: 8_351_812
b = galaxy_field(15, [
(0.5,0),
(5,0),
(12,0),
(9,0.5),
(14,0.5),
(2.5,1),
(7,1),
(11,1),
(5.5,1.5),
(4,2),
(12,2),
(7.5,2.5),
(7,4),
(9.5,4),
(12,4.5),
(0.5,5),
(4,5),
(5.5,5.5),
(7.5,5.5),
(14,5.5),
(3.5,6),
(10,6),
(14,7),
(2.5,7.5),
(8.5,7.5),
(10.5,7.5),
(2,9),
(7,9),
(13.5,9),
(6,9.5),
(1,10),
(12,10),
(3.5,10.5),
(14,11),
(7.5,11.5),
(9,11.5),
(11.5,11.5),
(10,12),
(13,12),
(0.5,12.5),
(4.5,12.5),
(2,13.5),
(8,13.5),
(10.5,13.5),
(13,13.5),
(5.5,14)
])

b = galaxy_field(10, [(5,0.5), (3.5,1), (7,1), (0,1.5), (1.5,2.5), (4,2.5), (7.5,3), (9,3), (0,4), (5,4), (3,5), (8,5), (0.5,7), (4,7), (7,7), (2,7.5), (6,8), (8.5,8), (4,8.5), (0.5,9), (3,9)])

print('initial board:')
b.show(showgrid=True, showborder=False)

b.solve()

if b.is_solved():
  print('Board solved:')
  b.show(showgrid=False, showborder=True, showunknown=True)
else:
  print('Solving failed:')
  b.show(showgrid=True, showborder=False)


print(f'{b.difficulty = }')

