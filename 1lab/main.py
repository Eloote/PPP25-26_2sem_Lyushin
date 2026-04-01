class Piece:
    def __init__(self, color, row, col):
        self.color = color
        self.row = row
        self.col = col
        self.has_moved = False

    def move_to(self, row, col):
        self.row = row
        self.col = col
        self.has_moved = True


class Figure1(Piece):
    def get_valid_moves(self, board):
        moves = []
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            r, c = self.row + dr * 2, self.col + dc * 2
            if 0 <= r < 8 and 0 <= c < 8:
                p = board.get_piece(r, c)
                if not p or p.color != self.color:
                    moves.append((r, c))
        return moves


class Figure2(Piece):
    def get_valid_moves(self, board):
        moves = []
        for dr, dc in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            r, c = self.row + dr * 2, self.col + dc * 2
            if 0 <= r < 8 and 0 <= c < 8:
                p = board.get_piece(r, c)
                if not p or p.color != self.color:
                    moves.append((r, c))
        return moves


class Figure3(Piece):
    def get_valid_moves(self, board):
        moves = []
        for dr, dc in [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1), (1, 1), (1, -1), (-1, 1),
                       (-1, -1)]:
            r, c = self.row + dr, self.col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                p = board.get_piece(r, c)
                if not p or p.color != self.color:
                    moves.append((r, c))
        return moves


class Pawn(Piece):
    def get_valid_moves(self, board):
        moves = []
        d = -1 if self.color == 'white' else 1
        r = self.row + d
        if 0 <= r < 8 and not board.get_piece(r, self.col):
            moves.append((r, self.col))
            if not self.has_moved and 0 <= r + d < 8 and not board.get_piece(r + d, self.col):
                moves.append((r + d, self.col))
        for dc in [-1, 1]:
            r, c = self.row + d, self.col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                p = board.get_piece(r, c)
                if p and p.color != self.color:
                    moves.append((r, c))
        return moves

    def get_attacked(self, board):
        d = -1 if self.color == 'white' else 1
        return [(self.row + d, self.col + dc) for dc in [-1, 1] if 0 <= self.row + d < 8 and 0 <= self.col + dc < 8]


class Rook(Piece):
    def get_valid_moves(self, board):
        moves = []
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            for i in range(1, 8):
                r, c = self.row + dr * i, self.col + dc * i
                if not (0 <= r < 8 and 0 <= c < 8): break
                p = board.get_piece(r, c)
                if not p:
                    moves.append((r, c))
                elif p.color != self.color:
                    moves.append((r, c)); break
                else:
                    break
        return moves


class Knight(Piece):
    def get_valid_moves(self, board):
        moves = []
        for dr, dc in [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]:
            r, c = self.row + dr, self.col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                p = board.get_piece(r, c)
                if not p or p.color != self.color:
                    moves.append((r, c))
        return moves


class Bishop(Piece):
    def get_valid_moves(self, board):
        moves = []
        for dr, dc in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            for i in range(1, 8):
                r, c = self.row + dr * i, self.col + dc * i
                if not (0 <= r < 8 and 0 <= c < 8): break
                p = board.get_piece(r, c)
                if not p:
                    moves.append((r, c))
                elif p.color != self.color:
                    moves.append((r, c)); break
                else:
                    break
        return moves


class Queen(Piece):
    def get_valid_moves(self, board):
        return Rook.get_valid_moves(self, board) + Bishop.get_valid_moves(self, board)


class King(Piece):
    def get_valid_moves(self, board):
        moves = []
        for dr, dc in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            r, c = self.row + dr, self.col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                p = board.get_piece(r, c)
                if not p or p.color != self.color:
                    moves.append((r, c))
        return moves


class CheckerPiece:
    def __init__(self, color, row, col):
        self.color = color
        self.row = row
        self.col = col
        self.is_king = False

    def move_to(self, row, col):
        self.row = row
        self.col = col
        if (self.color == 'white' and row == 0) or (self.color == 'black' and row == 7):
            self.is_king = True


class CheckersBoard:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.last_move = None
        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2:
                    self.grid[row][col] = CheckerPiece('white', row, col)
        for row in range(3):
            for col in range(8):
                if (row + col) % 2:
                    self.grid[row][col] = CheckerPiece('black', row, col)

    def get_piece(self, row, col):
        return self.grid[row][col] if 0 <= row < 8 and 0 <= col < 8 else None

    def move_piece(self, from_pos, to_pos):
        fr, fc = from_pos
        tr, tc = to_pos
        piece = self.grid[fr][fc]
        if not piece: return None
        self.last_move = (from_pos, to_pos)
        captured = None
        if abs(tr - fr) == 2:
            mr, mc = (fr + tr) // 2, (fc + tc) // 2
            captured = self.grid[mr][mc]
            self.grid[mr][mc] = None
        self.grid[tr][tc] = piece
        self.grid[fr][fc] = None
        piece.move_to(tr, tc)
        return captured

    def get_moves(self, piece):
        moves = []
        d = -1 if piece.color == 'white' else 1
        if not piece.is_king:
            for dc in [-1, 1]:
                r, c = piece.row + d, piece.col + dc
                if 0 <= r < 8 and 0 <= c < 8 and not self.get_piece(r, c):
                    moves.append((r, c))
            for dc in [-1, 1]:
                r, c = piece.row + d, piece.col + dc
                if 0 <= r < 8 and 0 <= c < 8:
                    target = self.get_piece(r, c)
                    if target and target.color != piece.color:
                        jr, jc = r + d, c + dc
                        if 0 <= jr < 8 and 0 <= jc < 8 and not self.get_piece(jr, jc):
                            moves.append((jr, jc))
        else:
            for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                for i in range(1, 8):
                    r, c = piece.row + dr * i, piece.col + dc * i
                    if not (0 <= r < 8 and 0 <= c < 8): break
                    target = self.get_piece(r, c)
                    if not target:
                        moves.append((r, c))
                    elif target.color != piece.color:
                        jr, jc = r + dr, c + dc
                        if 0 <= jr < 8 and 0 <= jc < 8 and not self.get_piece(jr, jc):
                            moves.append((jr, jc))
                        break
                    else:
                        break
        return moves

    def is_valid(self, piece, from_pos, to_pos):
        fr, fc = from_pos
        tr, tc = to_pos
        if abs(tr - fr) != abs(tc - fc):
            print("Ход должен быть по диагонали!")
            return False
        d = -1 if piece.color == 'white' else 1
        if not piece.is_king:
            if (piece.color == 'white' and tr >= fr) or (piece.color == 'black' and tr <= fr):
                print("Шашка может ходить только вперед!")
                return False
            if abs(tr - fr) == 1:
                if self.get_piece(tr, tc) is None: return True
                print("На этой клетке есть фигура!")
                return False
            if abs(tr - fr) == 2:
                mr, mc = (fr + tr) // 2, (fc + tc) // 2
                target = self.get_piece(mr, mc)
                if target and target.color != piece.color and self.get_piece(tr, tc) is None:
                    return True
                print("Нет фигуры для взятия!")
                return False
            print("Недопустимое расстояние!")
            return False
        return True

    def has_move(self, color):
        for row in range(8):
            for col in range(8):
                p = self.grid[row][col]
                if p and p.color == color and self.get_moves(p):
                    return True
        return False

    def threatened(self, row, col, color):
        for r in range(8):
            for c in range(8):
                p = self.grid[r][c]
                if p and p.color != color and (row, col) in self.get_moves(p):
                    return True
        return False

    def display(self):
        print("   a b c d e f g h")
        for row in range(8):
            print(f"{8 - row} ", end="")
            for col in range(8):
                p = self.grid[row][col]
                if p:
                    if p.is_king:
                        print(f"|{'⛃' if p.color == 'white' else '⛂'}", end="")
                    else:
                        print(f"|{'●' if p.color == 'white' else '◯'}", end="")
                else:
                    print("| ", end="")
            print("|")
        print("   a b c d e f g h")


class CheckersGame:
    def __init__(self):
        self.board = CheckersBoard()
        self.turn = 'white'
        self.over = False
        self.winner = None
        self.history = []

    def play(self):
        print("=" * 50)
        print("     ИГРА В ШАШКИ")
        print("=" * 50)
        print("ПРАВИЛА:")
        print("  - Белые шашки (●) СНИЗУ, ходят ВВЕРХ")
        print("  - Черные шашки (◯) СВЕРХУ, ходят ВНИЗ")
        print("  - Ход только по диагонали на 1 клетку вперед")
        print("  - Взятие: через одну клетку по диагонали")
        print("  - Дамка (⛃/⛂) ходит по диагонали на любое расстояние")
        print("=" * 50)
        print("Формат хода: c5d4 (откуда и куда)")
        print("Пример: c5d4 - ход белой шашки вверх-вправо")
        print("Команды: exit - выход, restart - новая игра, back - отменить ход, menu - главное меню")
        print("=" * 50)

        while True:
            self.board.display()

            threatened = []
            for r in range(8):
                for c in range(8):
                    p = self.board.grid[r][c]
                    if p and p.color == self.turn and self.board.threatened(r, c, self.turn):
                        threatened.append((r, c))
            if threatened:
                print("\n⚠️ ФИГУРЫ ПОД БОЕМ:")
                threat_str = [f"{chr(c + ord('a'))}{8 - r}" for r, c in threatened]
                print("  " + ", ".join(threat_str))

            if self.over:
                print(f"\nПОБЕДА! {'Белые' if self.winner == 'white' else 'Черные'} выиграли!")
                cmd = input("\nrestart - новая игра, menu - главное меню, exit - выход: ").strip().lower()
                if cmd == 'restart':
                    self.__init__()
                    continue
                elif cmd == 'menu':
                    return
                elif cmd == 'exit':
                    exit()
                else:
                    break

            print(f"\nХод {'БЕЛЫХ' if self.turn == 'white' else 'ЧЕРНЫХ'}")
            move = input("Введите ход или команду: ").strip().lower()

            if move == 'exit':
                exit()
            elif move == 'restart':
                self.__init__()
                continue
            elif move == 'menu':
                return
            elif move == 'back':
                if self.history:
                    f, t, p, c = self.history.pop()
                    self.board.grid[f[0]][f[1]] = p
                    self.board.grid[t[0]][t[1]] = None
                    p.row, p.col = f
                    if c:
                        mr, mc = (f[0] + t[0]) // 2, (f[1] + t[1]) // 2
                        self.board.grid[mr][mc] = c
                    self.turn = 'black' if self.turn == 'white' else 'white'
                    self.over = False
                    print("Ход отменен!")
                else:
                    print("Нет ходов для отмены!")
                continue

            if len(move) < 4:
                print("Ошибка! Формат: c5d4")
                continue

            try:
                fc, fr = ord(move[0]) - ord('a'), 8 - int(move[1])
                tc, tr = ord(move[2]) - ord('a'), 8 - int(move[3])
                if not (0 <= fr < 8 and 0 <= fc < 8 and 0 <= tr < 8 and 0 <= tc < 8):
                    print("Вне доски!")
                    continue
            except:
                print("Ошибка! Формат: c5d4")
                continue

            p = self.board.get_piece(fr, fc)
            if not p:
                print("Здесь нет фигуры!")
                continue
            if p.color != self.turn:
                print("Сейчас не ваш ход!")
                continue
            if not self.board.is_valid(p, (fr, fc), (tr, tc)):
                continue

            captured = self.board.move_piece((fr, fc), (tr, tc))
            self.history.append(((fr, fc), (tr, tc), p, captured))

            nt = 'black' if self.turn == 'white' else 'white'
            if not self.board.has_move(nt):
                self.over = True
                self.winner = self.turn
            else:
                self.turn = nt
            print("Ход принят")


class Board:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.white_king = (7, 4)
        self.black_king = (0, 4)
        self.setup()

    def setup(self):
        for col in range(8):
            self.grid[6][col] = Pawn('white', 6, col)
            self.grid[1][col] = Pawn('black', 1, col)

        pieces = [(Rook, 0), (Knight, 1), (Bishop, 2), (Queen, 3), (King, 4), (Bishop, 5), (Knight, 6), (Rook, 7)]
        for cls, col in pieces:
            self.grid[7][col] = cls('white', 7, col)
            self.grid[0][col] = cls('black', 0, col)

    def get_piece(self, row, col):
        return self.grid[row][col] if 0 <= row < 8 and 0 <= col < 8 else None

    def move_piece(self, from_pos, to_pos):
        fr, fc = from_pos
        tr, tc = to_pos
        p = self.grid[fr][fc]
        if not p: return None
        if isinstance(p, King):
            if p.color == 'white':
                self.white_king = (tr, tc)
            else:
                self.black_king = (tr, tc)
        captured = self.grid[tr][tc]
        self.grid[tr][tc] = p
        self.grid[fr][fc] = None
        p.move_to(tr, tc)
        return captured

    def in_check(self, color):
        king = self.white_king if color == 'white' else self.black_king
        for r in range(8):
            for c in range(8):
                p = self.grid[r][c]
                if p and p.color != color:
                    attacked = p.get_attacked(self) if hasattr(p, 'get_attacked') else p.get_valid_moves(self)
                    if king in attacked: return True
        return False

    def threatened(self, row, col, color):
        for r in range(8):
            for c in range(8):
                p = self.grid[r][c]
                if p and p.color != color:
                    attacked = p.get_attacked(self) if hasattr(p, 'get_attacked') else p.get_valid_moves(self)
                    if (row, col) in attacked: return True
        return False

    def copy(self):
        b = Board()
        b.grid = [[None for _ in range(8)] for _ in range(8)]
        for r in range(8):
            for c in range(8):
                p = self.grid[r][c]
                if p:
                    cls = p.__class__
                    np = cls(p.color, r, c)
                    np.has_moved = p.has_moved
                    b.grid[r][c] = np
                    if isinstance(p, King):
                        if p.color == 'white':
                            b.white_king = (r, c)
                        else:
                            b.black_king = (r, c)
        return b

    def is_legal(self, from_pos, to_pos, color):
        b = self.copy()
        b.move_piece(from_pos, to_pos)
        return not b.in_check(color)

    def has_legal(self, color):
        for r in range(8):
            for c in range(8):
                p = self.grid[r][c]
                if p and p.color == color:
                    for m in p.get_valid_moves(self):
                        if self.is_legal((r, c), m, color):
                            return True
        return False

    def display(self):
        print("   a b c d e f g h")
        for row in range(8):
            print(f"{8 - row} ", end="")
            for col in range(8):
                p = self.grid[row][col]
                if p:
                    if isinstance(p, Pawn):
                        s = '♟' if p.color == 'white' else '♙'
                    elif isinstance(p, Rook):
                        s = '♜' if p.color == 'white' else '♖'
                    elif isinstance(p, Knight):
                        s = '♞' if p.color == 'white' else '♘'
                    elif isinstance(p, Bishop):
                        s = '♝' if p.color == 'white' else '♗'
                    elif isinstance(p, Queen):
                        s = '♛' if p.color == 'white' else '♕'
                    elif isinstance(p, King):
                        s = '♚' if p.color == 'white' else '♔'
                    elif isinstance(p, Figure1):
                        s = '1' if p.color == 'white' else '7'
                    elif isinstance(p, Figure2):
                        s = '2' if p.color == 'white' else '8'
                    elif isinstance(p, Figure3):
                        s = '3' if p.color == 'white' else '9'
                    else:
                        s = '?'
                    print(f"|{s}", end="")
                else:
                    print("| ", end="")
            print("|")
        print("   a b c d e f g h")


class ChessGame:
    def __init__(self):
        self.board = Board()
        self.turn = 'white'
        self.over = False
        self.winner = None
        self.history = []

    def play(self):
        print("=" * 50)
        print("     ШАХМАТНЫЙ СИМУЛЯТОР")
        print("=" * 50)
        print("Формат хода: e2e4")
        print("♟/♙ - пешка: сначала на 2 клетки, потом на 1, бьет по диагонали")
        print("♞/♘ - конь: ходит буквой Г")
        print("♜/♖ - ладья: по горизонтали и вертикали")
        print("♝/♗ - слон: по диагонали")
        print("♛/♕ - ферзь: как ладья и слон")
        print("♚/♔ - король: на 1 клетку в любую сторону")
        print("=" * 50)
        print("Команды: exit - выход, restart - новая игра, back - отменить ход")
        print("         menu - главное меню, up - заменить фигуры справа на новые")
        print("=" * 50)
        print("НОВЫЕ ФИГУРЫ (после команды up):")
        print("  1 (белые) / 7 (черные) - ходит как ладья на 2 клетки")
        print("  2 (белые) / 8 (черные) - ходит как слон на 2 клетки")
        print("  3 (белые) / 9 (черные) - ходит как конь или на 1 клетку по диагонали")
        print("=" * 50)

        while True:
            self.board.display()

            threatened = []
            for r in range(8):
                for c in range(8):
                    p = self.board.grid[r][c]
                    if p and p.color == self.turn and self.board.threatened(r, c, self.turn):
                        threatened.append((r, c))
            if threatened:
                print("\n⚠️ ФИГУРЫ ПОД БОЕМ:")
                threat_str = []
                for r, c in threatened:
                    p = self.board.grid[r][c]
                    if isinstance(p, Pawn):
                        s = '♟' if p.color == 'white' else '♙'
                    elif isinstance(p, Rook):
                        s = '♜' if p.color == 'white' else '♖'
                    elif isinstance(p, Knight):
                        s = '♞' if p.color == 'white' else '♘'
                    elif isinstance(p, Bishop):
                        s = '♝' if p.color == 'white' else '♗'
                    elif isinstance(p, Queen):
                        s = '♛' if p.color == 'white' else '♕'
                    elif isinstance(p, King):
                        s = '♚' if p.color == 'white' else '♔'
                    elif isinstance(p, Figure1):
                        s = '1' if p.color == 'white' else '7'
                    elif isinstance(p, Figure2):
                        s = '2' if p.color == 'white' else '8'
                    elif isinstance(p, Figure3):
                        s = '3' if p.color == 'white' else '9'
                    else:
                        s = '?'
                    threat_str.append(f"{chr(c + ord('a'))}{8 - r}({s})")
                print("  " + ", ".join(threat_str))

            if self.board.in_check(self.turn):
                k = self.board.white_king if self.turn == 'white' else self.board.black_king
                print(f"\n👑 ШАХ КОРОЛЮ на {chr(k[1] + ord('a'))}{8 - k[0]}!")

            if self.over:
                print(f"\nМАТ! {'Белые' if self.winner == 'white' else 'Черные'} победили!")
                cmd = input("\nrestart - новая игра, menu - главное меню, exit - выход: ").strip().lower()
                if cmd == 'restart':
                    self.__init__()
                    continue
                elif cmd == 'menu':
                    return
                elif cmd == 'exit':
                    exit()
                else:
                    break

            print(f"\nХод {'БЕЛЫХ' if self.turn == 'white' else 'ЧЕРНЫХ'}")
            move = input("Введите ход или команду: ").strip().lower()

            if move == 'exit':
                exit()
            elif move == 'restart':
                self.__init__()
                continue
            elif move == 'menu':
                return
            elif move == 'back':
                if self.history:
                    f, t, p, c = self.history.pop()
                    self.board.grid[f[0]][f[1]] = p
                    self.board.grid[t[0]][t[1]] = c
                    p.row, p.col = f
                    if isinstance(p, King):
                        if p.color == 'white':
                            self.board.white_king = f
                        else:
                            self.board.black_king = f
                    self.turn = 'black' if self.turn == 'white' else 'white'
                    self.over = False
                    print("Ход отменен!")
                else:
                    print("Нет ходов для отмены!")
                continue
            elif move == 'up':
                for r in range(8):
                    for c in [5, 6, 7]:
                        p = self.board.grid[r][c]
                        if p and not isinstance(p, (King, Pawn)):
                            if p.color == 'white':
                                if c == 5:
                                    self.board.grid[r][c] = Figure1('white', r, c)
                                elif c == 6:
                                    self.board.grid[r][c] = Figure2('white', r, c)
                                else:
                                    self.board.grid[r][c] = Figure3('white', r, c)
                            else:
                                if c == 5:
                                    self.board.grid[r][c] = Figure1('black', r, c)
                                elif c == 6:
                                    self.board.grid[r][c] = Figure2('black', r, c)
                                else:
                                    self.board.grid[r][c] = Figure3('black', r, c)
                print("Фигуры справа заменены на новые!")
                continue

            if len(move) < 4:
                print("Ошибка! Формат: e2e4")
                continue

            try:
                fc, fr = ord(move[0]) - ord('a'), 8 - int(move[1])
                tc, tr = ord(move[2]) - ord('a'), 8 - int(move[3])
                if not (0 <= fr < 8 and 0 <= fc < 8 and 0 <= tr < 8 and 0 <= tc < 8):
                    print("Вне доски!")
                    continue
            except:
                print("Ошибка! Формат: e2e4")
                continue

            p = self.board.get_piece(fr, fc)
            if not p or p.color != self.turn:
                print("Недопустимый ход!")
                continue
            if (tr, tc) not in p.get_valid_moves(self.board):
                print("Недопустимый ход!")
                continue
            if not self.board.is_legal((fr, fc), (tr, tc), self.turn):
                print("Король под шахом!")
                continue

            captured = self.board.grid[tr][tc]
            self.board.move_piece((fr, fc), (tr, tc))
            self.history.append(((fr, fc), (tr, tc), p, captured))

            nt = 'black' if self.turn == 'white' else 'white'
            if self.board.has_legal(nt):
                self.turn = nt
            else:
                if self.board.in_check(nt):
                    self.over = True
                    self.winner = self.turn
                else:
                    print("Пат! Ничья!")
                    break
            print("Ход принят")


def show_menu():
    print("\n" + "=" * 50)
    print("     ГЛАВНОЕ МЕНЮ")
    print("=" * 50)
    print("1 - Шахматы")
    print("2 - Шашки")
    print("exit - Выход")
    print("=" * 50)


def main():
    while True:
        show_menu()
        choice = input("> ").strip().lower()

        if choice == '1' or choice == 'шахматы':
            game = ChessGame()
            game.play()
        elif choice == '2' or choice == 'шашки':
            game = CheckersGame()
            game.play()
        elif choice == 'exit':
            print("Выход из игры...")
            break
        else:
            print("Неверный выбор! Попробуйте снова.")


if __name__ == "__main__":
    main()
