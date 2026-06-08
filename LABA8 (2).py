import tkinter as tk
import random

# Константы игры
WIDTH = 600          # ширина окна
HEIGHT = 400         # высота окна
CELL_SIZE = 20       # размер клетки (пикселей)
DELAY = 150          # задержка между кадрами (мс)

# Цвета
BG_COLOR = "black"
SNAKE_COLOR = "green"
HEAD_COLOR = "dark green"
FOOD_COLOR = "red"
TEXT_COLOR = "white"

# Направления
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


# Собственные исключения
class GameOverError(Exception):
    """Выбрасывается при столкновении змейки со стеной или своим телом."""
    pass


class InvalidDirectionError(Exception):
    """Выбрасывается при попытке разворота на 180 градусов."""
    pass


class Snake:
    """Управляет змейкой."""
    def __init__(self, start_pos, start_dir):
        self.body = [start_pos]          # список координат (x, y) от головы к хвосту
        self.direction = start_dir       # текущее направление движения
        self.grow_flag = False           # нужно ли увеличить длину

    @property
    def head(self):
        return self.body[0]

    def change_direction(self, new_dir):
        """Меняет направление, если это не противоположное направление."""
        if (new_dir[0] == -self.direction[0] and new_dir[1] == -self.direction[1]):
            raise InvalidDirectionError("Разворот на 180° запрещён")
        self.direction = new_dir

    def move(self):
        """Перемещает змейку."""
        hx, hy = self.head
        dx, dy = self.direction
        new_head = (hx + dx * CELL_SIZE, hy + dy * CELL_SIZE)
        self.body.insert(0, new_head)
        if not self.grow_flag:
            self.body.pop()
        else:
            self.grow_flag = False

    def grow(self):
        """Увеличивает длину змейки при следующем движении."""
        self.grow_flag = True

    def check_collision(self, width, height):
        """Проверка столкновения со стенами или своим телом."""
        hx, hy = self.head
        # Стена
        if hx < 0 or hx >= width or hy < 0 or hy >= height:
            return True
        # Самостолкновение: голова врезается в тело (игнорируем голову в списке)
        if self.head in self.body[1:]:
            return True
        return False

    def draw(self, canvas):
        """Рисует змейку."""
        for i, (x, y) in enumerate(self.body):
            color = HEAD_COLOR if i == 0 else SNAKE_COLOR
            canvas.create_rectangle(x, y, x + CELL_SIZE, y + CELL_SIZE,
                                    fill=color, outline=BG_COLOR)


class Food:
    """Еда для змейки."""
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.position = (0, 0)
        self.randomize()

    def randomize(self, snake_body=None):
        """Генерирует случайную позицию (если передан snake_body – избегает пересечения)."""
        max_x = self.width - CELL_SIZE
        max_y = self.height - CELL_SIZE
        while True:
            x = random.randrange(0, max_x + 1, CELL_SIZE)
            y = random.randrange(0, max_y + 1, CELL_SIZE)
            if snake_body is None or (x, y) not in snake_body:
                self.position = (x, y)
                break

    def draw(self, canvas):
        x, y = self.position
        canvas.create_rectangle(x, y, x + CELL_SIZE, y + CELL_SIZE,
                                fill=FOOD_COLOR, outline=BG_COLOR)


class SnakeGame:
    """Основной класс игры (GUI на tkinter)."""
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Змейка")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT, bg=BG_COLOR)
        self.canvas.pack()

        # Панель с информацией об игре
        self.info_frame = tk.Frame(self.root, bg=BG_COLOR)
        self.info_frame.pack(fill=tk.X)

        self.score_label = tk.Label(self.info_frame, text="Счёт: 0", fg=TEXT_COLOR,
                                    bg=BG_COLOR, font=("Arial", 14))
        self.score_label.pack(side=tk.LEFT, padx=10, pady=5)

        self.status_label = tk.Label(self.info_frame, text="Игра: активна", fg=TEXT_COLOR,
                                     bg=BG_COLOR, font=("Arial", 12))
        self.status_label.pack(side=tk.RIGHT, padx=10, pady=5)

        # Начальное состояние
        start_x = WIDTH // 2 // CELL_SIZE * CELL_SIZE
        start_y = HEIGHT // 2 // CELL_SIZE * CELL_SIZE
        self.snake = Snake((start_x, start_y), RIGHT)
        self.food = Food(WIDTH, HEIGHT)
        self.food.randomize(self.snake.body)
        self.score = 0
        self.game_running = True
        self.after_id = None

        # Привязка клавиш
        self.root.bind("<Up>", lambda e: self.change_direction(UP))
        self.root.bind("<Down>", lambda e: self.change_direction(DOWN))
        self.root.bind("<Left>", lambda e: self.change_direction(LEFT))
        self.root.bind("<Right>", lambda e: self.change_direction(RIGHT))
        self.root.bind("<Escape>", lambda e: self.quit_game())
        self.root.protocol("WM_DELETE_WINDOW", self.quit_game)

        # Запуск игрового цикла
        self.game_loop()

    def change_direction(self, new_dir):
        """Обрабатывает изменение направления (игнорирует ошибки разворота)."""
        if not self.game_running:
            return
        try:
            self.snake.change_direction(new_dir)
        except InvalidDirectionError:
            pass

    def update(self):
        """Обновляет состояние игры (движение, поедание еды, проверки)."""
        if not self.game_running:
            return

        self.snake.move()

        # Проверка столкновений
        if self.snake.check_collision(WIDTH, HEIGHT):
            self.game_over()
            return

        # Поедание еды
        if self.snake.head == self.food.position:
            self.snake.grow()
            self.score += 1
            self.score_label.config(text=f"Счёт: {self.score}")
            self.food.randomize(self.snake.body)   # новая еда не на теле змейки

    def draw(self):
        """Полная перерисовка холста."""
        self.canvas.delete("all")
        self.snake.draw(self.canvas)
        self.food.draw(self.canvas)

    def game_loop(self):
        """Основной цикл, вызывается через after."""
        if self.game_running:
            try:
                self.update()
                self.draw()
            except GameOverError:
                self.game_over()
                return
            self.after_id = self.root.after(DELAY, self.game_loop)

    def game_over(self):
        """Обработка конца игры."""
        if not self.game_running:
            return
        self.game_running = False
        self.status_label.config(text="Игра: GAME OVER")
        # Показываем надпись на холсте
        self.canvas.create_text(WIDTH // 2, HEIGHT // 2 - 20,
                                text="GAME OVER", fill="red", font=("Arial", 24, "bold"))
        self.canvas.create_text(WIDTH // 2, HEIGHT // 2 + 20,
                                text=f"Финальный счёт: {self.score}",
                                fill="white", font=("Arial", 16))
        self.canvas.create_text(WIDTH // 2, HEIGHT // 2 + 60,
                                text="Нажмите ESC для выхода",
                                fill="light gray", font=("Arial", 12))

    def quit_game(self):
        """Корректное завершение игры."""
        if self.after_id:
            self.root.after_cancel(self.after_id)
        self.root.destroy()

    def run(self):
        """Запуск приложения."""
        self.root.mainloop()


if __name__ == "__main__":
    game = SnakeGame()
    game.run()
