theBoard = {'7':' ','8':' ','9':'',
            '4':' ','5':' ','6':' ',
            '1':' ','2':' ','3':' '}

def printBoard(board):
    print(board['7'] + '|' + board['8'] + '|' + board['9'])
    print('-+-+')
    print(board['4'] + '|' + board['5'] + '|' + board['6'])
    print('-+-+')
    print(board['1'] + '|' + board['2'] + '|' + board['3'])

turn = 'X'
for i in range(9):
    printBoard(theBoard)
    print('Turn for ' + turn + '. Move on which space ?')
    move = input()
    theBoard[move] = turn
    if turn == 'X':
        turn = 'O'
    else:
        turn = 'X'
printBoard(theBoard)

