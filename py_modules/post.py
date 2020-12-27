class Post:
    def __init__(self, post_dict: dict):
        self.name = post_dict['name']
        self.idx = post_dict['point_idx']
        self.post_idx = post_dict['idx']
        self.type = post_dict['type']
        if self.type == 1:
            # self.image_path = "pictures/city.png"
            self.armor = (post_dict['armor'], post_dict['armor_capacity'])
            self.population = (post_dict['population'], post_dict['population_capacity'])
            self.product = (post_dict['product'], post_dict['product_capacity'])
            self.upgrade_cost = post_dict['next_level_price']
        elif self.type == 2:
            # self.image_path = "pictures/shop.png"
            self.resource = (post_dict['product'], post_dict['product_capacity'])
            self.replenishment = post_dict['replenishment']
        elif self.type == 3:
            # self.image_path = "pictures/armour.png"
            self.resource = (post_dict['armor'], post_dict['armor_capacity'])
            self.replenishment = post_dict['replenishment']

        # image = pygame.image.load(self.resource_path()).convert_alpha()
        # self.image = pygame.transform.scale(image, (20, 20))

    # def resource_path(self):
    #     """ Get absolute path to resource, works for dev and for PyInstaller """
    #     try:
    #         # PyInstaller creates a temp folder and stores path in _MEIPASS
    #         base_path = sys._MEIPASS
    #     except Exception:
    #         base_path = os.path.abspath(".")
    #
    #     return os.path.join(base_path, self.image_path)

    def get_info(self) -> dict:
        info = {'name': [self.name], 'idx': [self.idx]}
        if self.type == 1:
            info['armor'] = [self.armor[0], self.armor[1]]
            info['population'] = [self.population[0], self.population[1]]
            info['product'] = [self.product[0], self.product[1]]
        elif self.type == 2:
            info['replenishment'] = [self.replenishment]
            info['product'] = [self.resource[0], self.resource[1]]
        elif self.type == 3:
            info['replenishment'] = [self.replenishment]
            info['armor'] = [self.resource[0], self.resource[1]]
        return info

    def update(self, post_dict: dict):
        if self.type == 1:
            self.armor = (post_dict['armor'], post_dict['armor_capacity'])
            if post_dict['population'] < self.population[0]:
                print('{0}/{1} people died from {2} food'.format(self.population[0]-post_dict['population'], self.population[0], self.product[0]))
            self.population = (post_dict['population'], post_dict['population_capacity'])
            self.product = (post_dict['product'], post_dict['product_capacity'])
            self.upgrade_cost = post_dict['next_level_price']
        elif self.type == 2:
            self.product = (post_dict['product'], post_dict['product_capacity'])
        elif self.type == 3:
            self.armor = (post_dict['armor'], post_dict['armor_capacity'])

    def get_income(self, last_visit, turns):
        income = min((turns - last_visit) * self.replenishment, self.resource[1])
        return income
