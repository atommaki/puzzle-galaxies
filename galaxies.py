#!/usr/bin/env python3


class bcolors:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

    COLORS=[ RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE]


class galaxy_field:

  def __init__(self,n,centers):
    self.centers = centers
    self.board_size = n
    self.board=[]
    for i in range(n):
      self.board.append([])
      for j in range(n):
        c = self.get_center_in_touch(j,i)
        self.board[i].append(c)

    change = True
    while change:
      change = False
      for i in range(n):
        for j in range(n):
          if self.board[i][j] != None:
            continue
          reachable = self.get_reachable_centers(j,i)
          possible = self.get_possible_centers(j,i)
          reachable_and_possible = reachable & possible
          #print(f'x={j=}  y={i=}  {reachable_and_possible=}  {reachable=}  {possible=}')
          if len(reachable_and_possible) == 1:
            c = reachable_and_possible.pop()
            self.board[i][j] = c
            mx, my = self.get_mirror_point(j,i, c[0], c[1])
            self.board[my][mx] = c
            change = True

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

  def get_reachable_centers(self, x,y, banned=set()):
    if self.board[y][x] != None:
      return { self.board[y][x] }
    reachable = set()
    check_list = { (x+1, y), (x-1, y), (x, y+1), (x, y-1) }
    #print(f'{x=}  {y=}  {check_list=}')
    for xx, yy in check_list:
      if (xx,yy) in banned or not self.is_on_board(xx,yy):
         continue
      reachable = reachable | self.get_reachable_centers(xx, yy, banned = banned | { (x,y) } | check_list)
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

  def show(self, showgrid=True):
    for i in range(-1, self.board_size*2):
      for j in range(-1, self.board_size*2):
        if self.is_center(j/2,i/2):
          print(f'{self.get_color((j/2,i/2))}o{bcolors.RESET} ', end='')
        else:
          if i/2 != i//2:
            if showgrid:
              print('- ', end='')
            else:
              print('  ', end='')
          elif j/2 != j//2:
            if showgrid:
              print('| ', end='')
            else:
              print('  ', end='')
          else:
            if j//2 < self.board_size and i//2 < self.board_size and i >= 0 and j >=0 and \
               self.board[i//2][j//2] != None:
                print(f'{self.get_color(self.board[i//2][j//2])}x{bcolors.RESET} ', end='')
            else:
                print('  ', end='')

      print()
#    print(self.board)



# 5x5 normal, ID= 1_758_394
b = galaxy_field(5,[(0.5,0), (3.5,0), (2.5,1), (0.5, 2.5), (4, 2.5), (2,3), (3,3.5)])
b.show(showgrid=True)

#print()
#print('2,2:')
#print(b.get_reachable_centers(2,2))


