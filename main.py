from speecher import Speecher

from chess import Board
from chess.engine import SimpleEngine


ENGINE_FILE_NAME = "engine/stockfish-windows-2022-x86-64-avx2.exe"
ALPHAS = {
    'б': 'b',
    'ц': 'c',
    'д': 'd',
    'е': 'e',
    'эф': 'f',
    'ж': 'g',
    'аш': 'h',
    'а': 'a'
}
PIECES = {
    'конь': 'N',
    'ладья': 'R',
    'пешка': 'P',
    'ферзь': 'Q',
    'королева': 'Q',
    'король': 'K',
    'слон': 'B'
}
TOKENS = PIECES.keys() | ALPHAS.keys() | set(str(elem) for elem in range(1, 9))

regular = "[a-h][1-8]x[a-h][1-8]"

def get_command(speecher: Speecher, board: Board) -> dict:
    
    correct_command = True
    
    data_command = speecher.recognize().lower().split()
    #tickets =
    command = ''.join([elem for elem in data_command if elem in TOKENS])
    
    for piece in PIECES.keys():
        command = command.replace(piece, PIECES[piece])
    for alpha in ALPHAS.keys():
        command = command.replace(alpha, ALPHAS[alpha])
    
    return {'command': command, 'correct_command': correct_command}
    

if __name__ == "__main__":
    
    board = Board()
    #engine = SimpleEngine.popen_uci(ENGINE_FILE_NAME)
    
    speecher = Speecher()
    print(1)
    
    is_running = True
    while is_running:
        command = get_command(speecher, board)
        print(command)

        if command['correct_command']:
            board.push_san(command[command])
            print(board)
        else:
            speecher.synthesize('Я вас не понял!')
