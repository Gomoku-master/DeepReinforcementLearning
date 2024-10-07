from game import Game

ROW_LEN, COL_LEN = 15, 15
g = Game()

count = 0
row, col = None, None

while True:
  count += 1
  print(f'\n\n{count}번째 수, 현재 board(흑: X, 백: O):')
  g.gameState.printBoard()

  cur_color = '흑' if g.currentPlayer == 1 else '백'
  print(f'{cur_color}의 차례입니다.')
  print('돌을 놓을 위치를 입력하세요. 행과 열은 0 이상 15 미만입니다. ex) 4, 3')

  while True:
    row, col = list(map(int, input('> ').split(',')))
    cur_action = row*COL_LEN + col

    if cur_action not in g.gameState._allowedActions():
      print('돌을 놓을 수 없는 위치입니다. 다시 입력하세요.\n')
    else:
      g.step(cur_action)
      break
  
  if g.gameState.isEndGame:
    g.gameState.printBoard()
    print('게임 끝')
    break
