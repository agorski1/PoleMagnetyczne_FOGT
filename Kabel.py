import numpy as np

class Kabel:
    def __init__(self, length, ctype="prosty"):
        self.coords = np.empty(shape=[0, 3])
        self.generate_cable(length, ctype)

    def generate_cable(self, length, ctype):
        if ctype == "prosty":
            self.generate_prosty(length)
        if ctype == "cewka":
            self.generate_cewka(length)
        if ctype == "sinus":
            self.generate_sinus(length)

    def generate_prosty(self, length):
        for i in range(length):
            self.coords = np.append(self.coords, [[i, 0, 0]], axis=0)


    def generate_sinus(self, length):
        for i in range(length):
            theta = i * (2 * np.pi) / 4
            new_x = i
            new_y = 0
            new_z = np.sin(theta / 8)
            new_xyz = [new_x, new_y, new_z]
            self.coords = np.append(self.coords, [new_xyz], axis=0)

    def generate_cewka(self, length):
        for i in range(length):
            theta = i * (2 * np.pi) / 2
            new_x = i
            new_y = np.cos(theta / 8)
            new_z = np.sin(theta / 8)
            new_xyz = [new_x, new_y, new_z]
            self.coords = np.append(self.coords, [new_xyz], axis=0)

    def get_coords(self, i):
        return self.coords[i]

    def get_cable_structure(self):
        return self.coords
