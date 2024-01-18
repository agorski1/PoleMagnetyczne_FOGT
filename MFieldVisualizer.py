import plotly.graph_objects as go
import csv
import plotly.express as px
import numpy as np
from PoleMagnetyczne import PoleMagnetyczne
import pandas as pd

class MFieldVisualizer:
    def __init__(self, cable_coords):
        self.cable_coords = cable_coords
        self.fig = px.line_3d(x=self.cable_coords[:, 0], y=self.cable_coords[:, 1], z=self.cable_coords[:, 2])
        self.MFpoints = []
        self.MFpoints_vectors = []


    def rotation_matrix_around_vector(self, rotation_vect, theta):
        v = rotation_vect / np.linalg.norm(rotation_vect)
        m1 = np.array([v[0]**2*(1-np.cos(theta)) + np.cos(theta), v[0]*v[1]*(1-np.cos(theta)) - v[2]*np.sin(theta), v[0]* v[2]*(1-np.cos(theta)) + v[1]*np.sin(theta)])
        m2 = np.array([v[0]*v[1]*(1-np.cos(theta))+v[2]*np.sin(theta), v[1]**2*(1-np.cos(theta))+np.cos(theta), v[1]*v[2]*(1-np.cos(theta))-v[0]*np.sin(theta)])
        m3 = np.array([v[0]*v[2]*(1-np.cos(theta))-v[1]*np.sin(theta), v[1]*v[2]*(1-np.cos(theta))+v[0]*np.sin(theta), v[2]**2*(1-np.cos(theta))+np.cos(theta)])

        rotation_matrix = np.array([m1, m2, m3])

        return rotation_matrix

    def find_vector(self, vector):
        perpend_vector = np.cross(vector, np.array([1, 1, 1]))
        perpend_vector_norm = perpend_vector / np.linalg.norm(perpend_vector) if np.linalg.norm(
            perpend_vector) != 0 else perpend_vector

        return perpend_vector_norm

    def find_points_around_line(self, start, end, points_per_circle, number_of_circles, radius):
        vect = end - start
        perp_vector = self.find_vector(vect) * radius
        rotation_matrix = self.rotation_matrix_around_vector(vect, (2 * np.pi) / (points_per_circle - 1))

        for j in range(number_of_circles+1):
            point = perp_vector + (j/number_of_circles * vect)
            self.MFpoints.append(point+start)
            pole_magnetyczne = PoleMagnetyczne.pole_w_punkcie_caly_odcinek(point+start, self.cable_coords)
            self.MFpoints_vectors.append(pole_magnetyczne)

            next_point = point
            for i in range(1, points_per_circle):
                next_point = np.dot(rotation_matrix, next_point)
                self.MFpoints.append(next_point+start)
                self.MFpoints_vectors.append(PoleMagnetyczne.pole_w_punkcie_caly_odcinek(next_point+start, self.cable_coords))

    def find_points_around_cable(self, points_per_circle, number_of_circles, radius):
        for i in range(self.cable_coords.shape[0]-1):
            self.find_points_around_line(self.cable_coords[i], self.cable_coords[i+1], points_per_circle, number_of_circles, radius)


    def coords_vectors_to_file(self, start, end, points_per_circle, number_of_circles, radius, coords_file, vectors_file):
        MFcoords = []
        MFvectors = []
        vect = end - start
        perp_vector = self.find_vector(vect) * radius
        rotation_matrix = self.rotation_matrix_around_vector(vect, (2 * np.pi) / (points_per_circle - 1))

        for j in range(number_of_circles + 1):
            point = perp_vector + (j / number_of_circles * vect)
            self.save_coords(coords_file, point+start)
            pole_magnetyczne = PoleMagnetyczne.pole_w_punkcie_caly_odcinek(point + start, self.cable_coords)
            self.save_vectors(vectors_file, pole_magnetyczne)
            next_point = point
            for i in range(1, points_per_circle):
                next_point = np.dot(rotation_matrix, next_point)
                self.save_coords(coords_file, next_point + start)
                self.save_vectors(vectors_file,
                    PoleMagnetyczne.pole_w_punkcie_caly_odcinek(next_point + start, self.cable_coords))





    def save_coords(self, coords_file, MFcoords):
        with open(coords_file, 'a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(MFcoords)

    def save_vectors(self, vectors_file, MFvectors):
        with open(vectors_file, 'a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(MFvectors)

    def save_coords_vectors_to_file(self, points_per_circle, number_of_circles, radius, coords_file, vectors_file):
        for i in range(self.cable_coords.shape[0] - 1):
            self.coords_vectors_to_file(self.cable_coords[i], self.cable_coords[i + 1], points_per_circle,
                                         number_of_circles, radius, coords_file, vectors_file)



    def cones_values(self):
        for i in range(len(self.MFpoints)):
            pole_w_punkcie = PoleMagnetyczne.pole_w_punkcie_caly_odcinek(np.array(self.MFpoints[i]), self.cable_coords)
            self.MFpoints_vectors.append(pole_w_punkcie)


    def addCones(self):
        self.find_points_around_cable(20,10,1)
        self.find_points_around_cable(20, 10, 1.1)
        self.find_points_around_cable(20, 10, 1.2)



        cone_coords = np.array(self.MFpoints)
        cone_vectors = np.array(self.MFpoints_vectors)
        print(cone_coords)
        print(cone_vectors)


        cones = go.Cone(x=cone_coords[:, 0], y=cone_coords[:, 1], z=cone_coords[:, 2], u=cone_vectors[:, 0], v=cone_vectors[:, 1], w=cone_vectors[:, 2], sizemode="scaled", sizeref=1)
        self.fig.add_trace(cones)

    def addConesFromFile(self, coords, vectors):
        coords = pd.read_csv(coords)
        vectors = pd.read_csv(vectors)

        cones = go.Cone(
            x=coords['x'],
            y=coords['y'],
            z=coords['z'],
            u=vectors['u'],
            v=vectors['v'],
            w=vectors['w'],
            sizemode="scaled",
            sizeref=3)
        self.fig.add_trace(cones)

    def draw(self):
        self.fig.show()
