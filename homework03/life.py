import pygame
from pygame.locals import *
import random
import copy


class GameOfLife:

    def __init__(self, width=640, height=480, cell_size=10, speed=10):
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_grid(self):
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.width, y))

    def run(self):
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        # Создание списка клеток
        self.clist = self.cell_list(randomize=True)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_grid()

            # Отображение списка
            self.draw_cell_list(self.clist)
            # Выполнение одного шага игры (обновление состояния ячеек)
            self.clist = self.update_cell_list(self.clist)

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def cell_list(self, randomize=False):
        """ Создание списка клеток.

        :param randomize: Если True, то создается список клеток, где
        каждая клетка равновероятно может быть живой (1) или мертвой (0).
        :return: Список клеток, представленный в виде матрицы
        """
        clist = []
        for h in range(self.height // self.cell_size):
            row = []
            for w in range(self.width // self.cell_size):
                if randomize:
                    row.append(random.randint(0, 1))
                if not randomize:
                    row.append(0)
            clist.append(row)
        return clist

    def draw_cell_list(self, clist):
        """ Отображение списка клеток

        :param clist: Список клеток для отрисовки, представленный в виде матрицы
        """
        white = pygame.Color('white')
        green = pygame.Color('green')
        for h in range(len(clist)):
            for w in range(len(clist[h])):
                y = h * self.cell_size
                x = w * self.cell_size
                if clist[h][w] == 0:
                    pygame.draw.rect(self.screen, white, [x, y, self.cell_size, self.cell_size])
                else:
                    pygame.draw.rect(self.screen, green, [x, y, self.cell_size, self.cell_size])
        pass

    def get_neighbours(self, cell):
        """ Вернуть список соседей для указанной ячейки

        :param cell: Позиция ячейки в сетке, задается кортежем вида (row, col)
        :return: Одномерный список ячеек, смежных к ячейке cell
        """
        neighbours = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                h = cell[0] + i
                w = cell[1] + j
                if i == 0 and j == 0:
                    continue
                if 0 <= w < self.cell_width and 0 <= h < self.cell_height:
                    neighbours.append(self.clist[h][w])
        return neighbours

    def update_cell_list(self, cell_list):
        """ Выполнить один шаг игры.

        Обновление всех ячеек происходит одновременно. Функция возвращает
        новое игровое поле.

        :param cell_list: Игровое поле, представленное в виде матрицы
        :return: Обновленное игровое поле
        """
        new_clist = copy.deepcopy(cell_list)
        for h in range(self.cell_height):
            for w in range(self.cell_width):
                neighbours = self.get_neighbours((h, w))
                alive_neighbours = sum(neighbours)
                if alive_neighbours != 2 and alive_neighbours != 3:
                    new_clist[h][w] = 0
                elif alive_neighbours == 3:
                    new_clist[h][w] = 1
        return new_clist

if __name__ == '__main__':
    game = GameOfLife(320, 240, 20)
    game.run()