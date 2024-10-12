import numpy as np

#####################################
######### 금수 판정용 함수들 #########
#####################################

def is_five(board, position, overline=False):
  # board의 position에 흑돌을 놓는 것으로 5가 완성되는지 확인
  # overline=True라면 6목 이상 장목이 완성되는지 확인

  directions = [(-1, 0), (0, 1), (-1, 1), (1, 1)]  # 상, 우, 우상, 우하 방향으로 연속된 흑돌의 개수를 센다. 
  signs = [1, -1]  # 각 direction에 대해서 그 반대 방향으로도 세줘야 함. 
  
  for dir in directions:
    count = 1  # position에 놓을 돌 포함, 연속된 돌의 개수

    for sign in signs:
      count += count_consecutive(board, position, tuple(sign*d for d in dir))

    if overline:
      if count > 5:
        return True
    elif count == 5:
      return True

  return False

def count_consecutive(board, position, dir):  
  # dir 방향(단방향)으로 연속된 흑돌의 개수 세서 리턴. position 칸은 제외한다. 

  rows, cols = 15, 15  # 계속 이렇게 하는 거 귀찮은데 GameState 프로퍼티로 rows, cols 만들어주거나 아니면 앞으로 무조건 15 * 15로 할 거라고 확정하면 좋을듯
  count = 0
  x, y = divmod(position, cols)
  dx, dy = dir

  while True:
    x, y = x + dx, y + dy
    
    if 0 <= x < rows and 0 <= y < cols:
      if board[x*cols + y] == 1:
        count += 1
      else:
        break
    else:  # 장외로 나가면 stop
      break

  return count

def is_double_four(board, position):
  # 44가 되는지 확인. 즉 각기 다른 4가 두 개 이상 완성되는지 확인

  directions = [(-1, 0), (0, 1), (-1, 1), (1, 1)]  # 상, 우, 우상, 우하
  four_count = 0
  
  for dir in directions:
    four_count += count_four(board, position, dir)

    if four_count >= 2:
      return True

  return False

def count_four(board, position, dir):  
  # dir 방향(양방향)으로 position을 포함하는 4의 개수 세기
  # 양방향으로 하는 이유? 5를 체크하는 것은 단방향으로 연속된 흑돌의 개수를 센 뒤 둘을 더하면 되지만 4 체크는 양쪽을 한 번에 고려해야 함
  # 4란? 한 수를 더 두면 연속된 5개가 되는 상태. 좌우 막혀있는지 여부는 상관 없음. 

  rows, cols = 15, 15
  temp_board = np.array(board)
  temp_board[position] = 1  # position에 흑돌을 놓는다고 가정. 
  targets = []
  count = 0

  x, y = divmod(position, cols)
  dx, dy = dir

  for i in range(-5, 6):  # position을 포함하여, 양방향 각 4칸씩, 총 9칸을 targets에 담는다. 그리고 양 끝 밖으로 한 칸씩도 targets에 담는다. 
    tx, ty = x + i*dx, y + i*dy

    if 0 <= tx < rows and 0 <= ty < cols:
      targets.append(temp_board[tx*cols + ty])
    else:
      targets.append(-1)  # 장외라면 백돌로 판정

  for i in range(1, 6):  # 9칸에서, 각 연속된 5칸씩을 sliding window(총 5회)
    if sum(targets[i:i+5]) == 4:  # 해당 5칸이 흑돌 4개 빈칸 1개라면
      if targets[i-1] != 1 and targets[i+5] != 1:  # 5칸의 양 끝의 옆에 흑돌이 없으면 4 확정
        count += 1
        if (targets[i] == 1 and targets[i+4] == 0) or (targets[i] == 0 and targets[i+4] == 1):  # 흑돌 4개가 연속인 4라면, dir 방향에서는 더 이상 4가 나올 수 없음
          break
  
  return count
      
def is_double_three(board, position):
  # 33이 되는지 확인. 즉 각기 다른 3이 두 개 이상 완성되는지 확인

  directions = [(-1, 0), (0, 1), (-1, 1), (1, 1)]  # 상, 우, 우상, 우하
  three_count = 0
  
  for dir in directions:
    if is_three(board, position, dir):
      three_count += 1

    if three_count >= 2:
      return True
    
  return False

def is_three(board, position, dir):
  # position에 놓을 때, dir 방향(양방향)으로 3이 되는지 체크
  # 3이란? 한 수를 더 두면 열린 4가 되는 상태. 
  # 열린 4란? 4목에서 양 끝이 막혀 있지 않은 상태
  # 어떠한 dir 방향으로 3은 최대 한 개만 나올 수 있기에 count할 필요 없음

  rows, cols = 15, 15
  temp_board = np.array(board)
  temp_board[position] = 1  # position에 흑돌을 놓는다고 가정. 
  targets = []

  x, y = divmod(position, cols)
  dx, dy = dir

  for i in range(-5, 6):  # position을 포함하여, 양방향 각 3칸씩, 총 7칸을 targets에 담는다. 그리고 양 끝 밖으로 두 칸씩도 targets에 담는다. 
    tx, ty = x + i*dx, y + i*dy

    if 0 <= tx < rows and 0 <= ty < cols:
      targets.append(temp_board[tx*cols + ty])
    else:
      targets.append(-1)  # 장외라면 백돌로 판정

  for i in range(2, 6):  # 7칸에서, 각 연속된 4칸씩을 sliding window(총 4번)
    if sum(targets[i:i+4]) == 3:  # 해당 4칸이 흑돌 3개 빈칸 1개라면
      if targets[i-1] == 0 and targets[i+4] == 0:  # 4칸의 양 끝의 옆이 빈칸이라면
        if targets[i-2] != 1 and targets[i+5] != 1:  # 거기서 한 칸 더 옆이 흑이 아니라면
          return True  # 3 확정
  
  return False

#####################################
#####################################
#####################################


# 금수 확인하고 싶은 board 만들기(_: 빈 칸, X: 흑돌, O: 백돌, P: 금수 확인 위치)
your_board = np.array([
  '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', 
  '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', 
  '_', '_', '_', 'X', '_', '_', 'P', 'X', 'X', '_', 'O', '_', '_', '_', '_', 
  '_', '_', '_', '_', '_', '_', 'X', '_', '_', '_', '_', '_', '_', '_', '_', 
  '_', '_', '_', '_', '_', '_', 'X', '_', '_', '_', '_', '_', '_', '_', '_', 
  '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', 
  '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', 
  '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', 
  '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', 
  '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', 
  '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', 
  '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', 
  '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', 
  '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', 
  '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_'
])

# 초기화용
hungry = np.array([
  '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', 
  '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', 
  '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', 
  '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', 
  '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', 
  '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', 
  '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', 
  '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', 
  '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', 
  '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', 
  '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', 
  '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', 
  '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', 
  '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', 
  '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_'
])

position = np.where(your_board == 'P')[0][0]
row, col = position // 15, position % 15

board = np.array([0] * 225)

for idx, val in enumerate(your_board):
  if val == '_':
    board[idx] = 0
  elif val == 'X':
    board[idx] = 1
  elif val == 'O':
    board[idx] = -1
  else:
    board[idx] = 0

allowed, geumsu = True, ''

if is_five(board, position):  # (position에 놓음으로써)오목을 완성할 수 있다면
  allowed = True
elif is_five(board, position, overline=True):  # 6목 이상의 장목이 된다면, 즉 position의 흑돌을 포함하여 6개 이상의 연속된 흑돌이 완성된다면
  allowed, geumsu = False, '장목'
elif is_double_four(board, position):  # 44가 된다면, 즉 각기 다른 4가 2개 이상 완성된다면
  allowed, geumsu = False, '44'
elif is_double_three(board, position):  # 33이 된다면, 즉 각기 다른 열린 3이 2개 이상 완성된다면
  allowed, geumsu = False, '33'
else:
  allowed = True

if allowed:
  print(f'해당 위치({row}, {col})는 금수가 아닙니다.')
else:
  print(f'해당 위치({row}, {col})는 금수입니다. 원인은 {geumsu}입니다.')
