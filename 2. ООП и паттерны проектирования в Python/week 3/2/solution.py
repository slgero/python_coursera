class System:
    def __init__(self):
        self.map = self.grid = [[0 for i in range(30)] for _ in range(20)]
        self.map[5][7] = 1  # Источники света
        self.map[5][2] = -1  # Стены

    def get_lightening(self, light_mapper):
        self.lightmap = light_mapper.lighten(self.map)

class Light:
    def __init__(self, dim):
        self.dim = dim  # Размер поля - кортеж
        self.grid = [[0 for i in range(dim[0])] for _ in range(dim[1])]
        self.lights = []
        self.obstacles = []

    def set_dim(self, dim):
        self.dim = dim
        self.grid = [[0 for i in range(dim[0])] for _ in range(dim[1])]

    def set_lights(self, lights):
        """Устанавливает массив источников света с заданными координатами"""
        self.lights = lights
        self.generate_lights()

    def set_obstacles(self, obstacles):
        """Устанавливает препятствия с заданными координатами"""
        self.obstacles = obstacles
        self.generate_lights()

    def generate_lights(self):
        """Рассчитывает освещенность с учетом источников и препятствий"""
        return self.grid.copy()


class MappingAdapter:
    def __init__(self, adaptee):
        self.adaptee = adaptee
        self.lights = [] # Координаты источников света
        self.obstacles = [] # Координаты препятсвий

    def lighten(self, grid):
        dim = (len(grid[0]), len(grid))
        self.adaptee.set_dim(dim)
        self.analyse_grid(dim, grid)
        self.adaptee.set_lights(self.lights)
        self.adaptee.set_obstacles(self.obstacles)
        return self.adaptee.grid

    def analyse_grid(self, dim, grid):
        """Находит и сохраняет координаты препятсвий и источников освещения"""
        for i in range(dim[0]):
            for j in range(dim[1]):
                if grid[j][i] == 1:
                    self.lights.append((i, j))
                if grid[j][i] == -1:
                    self.obstacles.append((i, j))


# s = System()
# light = Light((30, 20))
# adap = MappingAdapter(light)
# s.get_lightening(adap)
