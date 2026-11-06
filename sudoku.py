#K4ZU Minor python game project
import random
import tkinter as tk

SIZE = 9
BLANKS = 45  # how many cells to remove when making a puzzle


def is_valid(board, row, col, num):
    """True if num can go at (row, col) without breaking sudoku rules."""
    for i in range(SIZE):
        if board[row][i] == num or board[i][col] == num:
            return False
    box_row, box_col = row - row % 3, col - col % 3
    for r in range(box_row, box_row + 3):
        for c in range(box_col, box_col + 3):
            if board[r][c] == num:
                return False
    return True


def solve(board):
    """Fill the board in place. Random order makes every grid different."""
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == 0:
                numbers = list(range(1, 10))
                random.shuffle(numbers)
                for num in numbers:
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve(board):
                            return True
                        board[row][col] = 0
                return False
    return True


def new_puzzle():
    """Return (puzzle, solution) as two 9x9 grids."""
    board = [[0] * SIZE for _ in range(SIZE)]
    solve(board)
    solution = [row[:] for row in board]

    for _ in range(BLANKS):
        while True:
            row, col = random.randrange(SIZE), random.randrange(SIZE)
            if board[row][col] != 0:
                board[row][col] = 0
                break
    return board, solution


class Sudoku:
    def __init__(self, root):
        self.root = root
        root.title("Sudoku")

        # Black frame with small gaps between cells -> the grid lines.
        grid = tk.Frame(root, bg="black", padx=2, pady=2)
        grid.pack(padx=12, pady=12)

        self.labels = [[None] * SIZE for _ in range(SIZE)]
        for row in range(SIZE):
            for col in range(SIZE):
                label = tk.Label(grid, width=2, height=1, bg="white",
                                 font=("Arial", 26))
                # Wider gaps every three cells make the 3x3 boxes.
                label.grid(row=row, column=col,
                           padx=(3 if col in (3, 6) else 1, 0),
                           pady=(3 if row in (3, 6) else 1, 0))
                label.bind("<Button-1>", lambda e, r=row, c=col: self.select(r, c))
                self.labels[row][col] = label

        tk.Button(root, text="New Game", command=self.new_game).pack(pady=(0, 12))
        root.bind("<Key>", self.type_number)
        self.new_game()

    def new_game(self):
        self.puzzle, self.solution = new_puzzle()
        self.selected = None
        for row in range(SIZE):
            for col in range(SIZE):
                value = self.puzzle[row][col]
                self.labels[row][col].config(text=str(value) if value else "",
                                             fg="black", bg="white")

    def select(self, row, col):
        """Highlight a cell the player is allowed to fill in."""
        if self.puzzle[row][col] != 0:  # given number, not editable
            return
        if self.selected:
            self.labels[self.selected[0]][self.selected[1]].config(bg="white")
        self.selected = (row, col)
        self.labels[row][col].config(bg="#ffe9a8")

    def type_number(self, event):
        if not self.selected or event.char not in "123456789":
            return
        row, col = self.selected
        num = int(event.char)
        label = self.labels[row][col]

        if num == self.solution[row][col]:
            self.puzzle[row][col] = num  # lock it in
            label.config(text=str(num), fg="green", bg="white")
            self.selected = None
        else:
            label.config(text=str(num), fg="red")


if __name__ == "__main__":
    root = tk.Tk()
    Sudoku(root)
    root.mainloop()
