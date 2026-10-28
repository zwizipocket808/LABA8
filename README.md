ОТЧЁТ ПО ЛАБОРАТОРНОЙ РАБОТЕ
Задание: Игра «Змейка».

Условие: Разработать игру «Змейка» с графическим интерфейсом. Игровое поле — Canvas, змейка управляется стрелками клавиатуры, еда появляется в случайных местах, ведётся подсчёт очков, обрабатываются столкновения со стенами и собственным телом, игра корректно завершается. Дополнительные требования (объектно-ориентированная реализация): использование собственных исключений, managed-атрибуты (свойства @property), отдельные классы предметной области и основной класс игры, запрет разворота на 180 градусов, GUI-фреймворк — tkinter.

Описание проделанной работы: Был создан файл snake.py со следующей структурой.

Константы. Размеры окна WIDTH = 600, HEIGHT = 400, размер клетки CELL_SIZE = 20, задержка между кадрами DELAY = 150 мс. Цвета: BG_COLOR = "black", SNAKE_COLOR = "green", HEAD_COLOR = "dark green", FOOD_COLOR = "red", TEXT_COLOR = "white". Направления заданы кортежами: UP = (0, -1), DOWN = (0, 1), LEFT = (-1, 0), RIGHT = (1, 0).

Собственные исключения. GameOverError — выбрасывается при столкновении змейки со стеной или своим телом. InvalidDirectionError — выбрасывается при попытке разворота на 180 градусов.

Класс Snake. Хранит тело змейки self.body (список координат (x, y) от головы к хвосту), текущее направление self.direction и флаг роста self.grow_flag. Managed-атрибут head реализован через @property и возвращает self.body[0]. Метод change_direction(new_dir) проверяет, не является ли новое направление противоположным текущему (new_dir[0] == -self.direction[0] and new_dir[1] == -self.direction[1]), и при попытке разворота выбрасывает InvalidDirectionError. Метод move() вычисляет новую голову (hx + dx*CELL_SIZE, hy + dy*CELL_SIZE), вставляет её в начало списка и удаляет хвост, если не установлен флаг роста; при установленном флаге сбрасывает его. Метод grow() устанавливает grow_flag = True. Метод check_collision(width, height) возвращает True, если голова вышла за границы поля (hx < 0 or hx >= width or hy < 0 or hy >= height) или совпадает с одним из сегментов тела (self.head in self.body[1:]). Метод draw(canvas) рисует каждый сегмент прямоугольником CELL_SIZE × CELL_SIZE: голова — HEAD_COLOR, остальные — SNAKE_COLOR, контур — BG_COLOR.

Класс Food. Хранит размеры поля self.width, self.height и позицию self.position. В конструкторе вызывает randomize(). Метод randomize(snake_body=None) генерирует случайные координаты, кратные CELL_SIZE, в диапазоне поля; если передан snake_body, повторяет генерацию, пока позиция не окажется вне тела змейки. Метод draw(canvas) рисует еду прямоугольником CELL_SIZE × CELL_SIZE цветом FOOD_COLOR.

Класс SnakeGame. Основной класс с GUI на tkinter. В __init__ создаётся окно Tk с заголовком «Змейка» (resizable(False, False)), Canvas размером WIDTH × HEIGHT с фоном BG_COLOR, панель информации info_frame с score_label («Счёт: 0») и status_label («Игра: активна»). Начальная позиция змейки — центр поля, выровненный по сетке (WIDTH // 2 // CELL_SIZE * CELL_SIZE), направление — RIGHT. Создаются объекты Snake и Food (еда сразу генерируется вне тела змейки), счёт self.score = 0, флаг self.game_running = True, self.after_id = None. Клавиши <Up>, <Down>, <Left>, <Right> привязаны к change_direction, <Escape> — к quit_game, закрытие окна (WM_DELETE_WINDOW) также обрабатывается quit_game. В конце конструктора запускается game_loop().

Метод change_direction(new_dir) — если игра не активна, ничего не делает; иначе вызывает Snake.change_direction и перехватывает InvalidDirectionError (разворот на 180° просто игнорируется).

Метод update() — если игра не активна, выходит; иначе двигает змейку (snake.move()), проверяет столкновение (snake.check_collision(WIDTH, HEIGHT)) и при столкновении вызывает game_over(). При совпадении головы с позицией еды (self.snake.head == self.food.position) вызывает snake.grow(), увеличивает self.score, обновляет score_label и генерирует новую еду вне тела змейки (food.randomize(self.snake.body)).

Метод draw() — очищает холст (canvas.delete("all")) и заново рисует змейку и еду.

Метод game_loop() — если игра активна, вызывает update() и draw() (внутри try/except GameOverError), затем планирует следующий кадр через self.root.after(DELAY, self.game_loop) и сохраняет идентификатор в self.after_id.

Метод game_over() — если игра уже остановлена, выходит; иначе устанавливает game_running = False, меняет status_label на «Игра: GAME OVER» и выводит на холсте надписи «GAME OVER» (красным, 24 pt, bold), «Финальный счёт: N» (белым, 16 pt) и «Нажмите ESC для выхода» (светло-серым, 12 pt).

Метод quit_game() — если есть after_id, отменяет запланированный вызов (after_cancel), затем уничтожает окно (root.destroy).

Метод run() — запускает root.mainloop().

В блоке if __name__ == "__main__": создаётся объект SnakeGame и вызывается run(). Все требования выполнены: ООП-реализация с классами предметной области (Snake, Food) и основным классом игры (SnakeGame), managed-атрибут head через @property, собственные исключения GameOverError и InvalidDirectionError, запрет разворота на 180°, подсчёт очков, обработка столкновений и корректное завершение.

Скриншоты работы программы:


Главное окно программы (начало игры):
<img width="1092" height="597" alt="Снимок экрана 2026-10-28 205420" src="https://github.com/user-attachments/assets/7e02c9f4-f6ad-45dc-9e0c-f03358705265" />

Процесс игры (змейка, еда, счёт):
<img width="669" height="520" alt="image" src="https://github.com/user-attachments/assets/bb30196c-b7c2-4cd9-a1f9-98f76e260cd3" />

Экран Game Over (финальный счёт):
<img width="602" height="464" alt="image" src="https://github.com/user-attachments/assets/5051dc57-fb24-4453-aa1b-1b6de27641f1" />




