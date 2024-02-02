import sys
import random

class GomokuBot:
    def __init__(self, color):
        if (not (color == "흑" or color == "백")) :
            print("흑, 백이 입력되지 않았습니다. 게임을 종료합니다.")
            sys.exit(0)
        
        self.board = [['.' for _ in range(19)] for _ in range(19)]
        self.player = color  # 흑이 먼저 시작
        self.moves = []  # 수순 기록

    def print_board(self):
        for row in self.board:
            print(' '.join(row))
        print()

    def is_valid_move(self, x, y):
        return self.board[x][y] == '.'

    def make_move(self, x, y, player):
        if self.is_valid_move(x, y):
            self.board[x][y] = '흑' if player == '흑' else '백'
            self.moves.append((x, y, player))
            if self.check_win(x, y):
                print(f"{player} 승리!")
                return "win"
            return True
        return False

    def find_next_move(self):
        # 돌이 한 개 있을 때 주변의 유효한 빈 칸 찾기
        if len(self.moves) == 1:
            x, y, _ = self.moves[0]  # 현재 돌의 위치
            directions = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < 19 and 0 <= ny < 19 and self.board[nx][ny] == '.':
                    return nx, ny  # 유효한 빈 칸의 좌표 반환
        
        # 돌이 두 개 이상 연속된 경우 해당 방향의 다음 좌표 구하기
        for x, y, player in reversed(self.moves):  # 최근 수부터 확인
            for dx, dy in [(1, 0), (0, 1), (1, 1), (1, -1)]:
                count = 1
                # 해당 방향으로 돌이 연속되는지 확인
                while True:
                    nx, ny = x + count * dx, y + count * dy
                    if 0 <= nx < 19 and 0 <= ny < 19 and self.board[nx][ny] == player:
                        count += 1
                    else:
                        break
                if count >= 2:  # 2개 이상 연속되면
                    next_x, next_y = nx, ny  # 다음 좌표
                    if self.valid_position(next_x, next_y):
                        return next_x, next_y
                    else:  # 반대 방향의 좌표 구하기
                        opposite_x, opposite_y = x - dx, y - dy
                        if self.valid_position(opposite_x, opposite_y):
                            return opposite_x, opposite_y
            return None  # 유효한 수를 찾지 못한 경우
    
    def get_computer_move(self):
        # 수비 로직
        # 3개가 연속되는 자리의 다음자리를 막음.
        for i in range(19):
            for j in range(19):
                if self.board[i][j] != '.':
                    result = self.check_three_in_row(i, j)
                    if result:
                        return result

        next_move = self.find_next_move()

        if (next_move == None) :
            while(True) :
                x = random.randint(0, 18)
                y = random.randint(0, 18)
                if self.board[x][y] == '.':
                    return x, y
        else :
            return next_move

    def check_win(self, x, y):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # 가로, 세로, 대각선 방향
        for dx, dy in directions:
            count = 1
            # 현재 돌에서 양방향으로 검사
            for d in [1, -1]:
                step = 1
                while True:
                    nx, ny = x + step * dx * d, y + step * dy * d
                    if 0 <= nx < 19 and 0 <= ny < 19 and self.board[nx][ny] == self.board[x][y]:
                        count += 1
                        step += 1
                    else:
                        break
            if count >= 5:
                return True
        return False
    
    def valid_position(self, x, y):
        return 0 <= x < 19 and 0 <= y < 19 and self.board[x][y] == '.'

    def check_three_in_row(self, x, y):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # 가로, 세로, 대각선 방향
        for dx, dy in directions:
            for d in [1, -1]:
                count = 1
                step = 1
                while True:
                    nx, ny = x + step * dx * d, y + step * dy * d
                    if 0 <= nx < 19 and 0 <= ny < 19 and self.board[nx][ny] == self.board[x][y]:
                        count += 1
                        if count == 3:  # 3개의 돌이 연속되었는지 확인
                            next_x, next_y = x + (step + 1) * dx * d, y + (step + 1) * dy * d
                            prev_x, prev_y = x - dx * d, y - dy * d
                            # 다음 위치가 유효한지 확인
                            if self.valid_position(next_x, next_y):
                                return next_x, next_y
                            elif self.valid_position(prev_x, prev_y):  # 반대 방향의 유효성 확인
                                return prev_x, prev_y
                        step += 1
                    else:
                        break
        return None


    def play(self, x, y):
        if self.make_move(x, y, self.player) == "win":
            self.print_board()
            print(f"{self.player}이(가) 승리했습니다!")
            print("시스템을 종료합니다.")
            sys.exit(0)
        elif self.is_valid_move(x, y):
            print("유효하지 않은 수입니다. 다른 위치를 선택하세요.")
            return False

        self.print_board()
        self.player = '백' if self.player == '흑' else '흑'  # 플레이어 교체

        # 컴퓨터의 차례
        cx, cy = self.get_computer_move()
        if cx is not None and self.make_move(cx, cy, self.player) == "win":
            print(f"컴퓨터가 {cx}, {cy}에 두었습니다.")
            self.print_board()
            print(f"{self.player}가 승리했습니다!")
            return
        elif cx is not None:
            self.make_move(cx, cy, self.player)
            print(f"컴퓨터가 {cx}, {cy}에 두었습니다.")
            self.print_board()
            self.player = '백' if self.player == '흑' else '흑'  # 플레이어 교체
        else:
            print("게임 종료")

color = str(input("봇의 색을 정해주세요 (흑 or 백)"))

# 사용 예시
bot = GomokuBot(color="흑" if color == '백' else '백')

if (color == "흑") :
    print("봇이 흑돌임으로 먼저 둡니다.")
    cx, cy = bot.get_computer_move()
    
    while(not bot.is_valid_move(cx, cy)) :
        cx, cy = bot.get_computer_move()

    bot.make_move(cx, cy, color)
    print(f"컴퓨터가 {cx}, {cy}에 두었습니다.")
    bot.print_board()

while(1) :

    isPositionOk = False
    while(not isPositionOk) :
        input_str = input("Enter your move (e.g., 2, 4): ")

        # 입력 문자열을 쉼표로 분리하고 공백 제거 후 정수 변환
        try :
            x, y = map(int, input_str.split(','))
            if (not bot.is_valid_move(x, y)):
                print("이미 둬져있는 자리입니다. 다시 입력해주세요")
                continue

            isPositionOk = True
        except Exception as ex:
            print("입력값이 잘못되었습니다. 다시 입력해주세요")

    bot.play(x, y)