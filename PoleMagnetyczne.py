import numpy as np

class PoleMagnetyczne:

    miu_0 = 4 * np.pi * 1e-7


    @classmethod
    def pole_w_punkcie_odcinek(cls, coordsdB, I, start_point, end_point):
        dl = end_point - start_point
        r = coordsdB - start_point
        norm_r = np.linalg.norm(r)
        dB = np.array([0,0,0])

        if(norm_r != 0):
            dB = cls.miu_0/(4 * np.pi) * I * (np.cross(dl,r))/((norm_r)**3)
        # print(np.cross(dl,r))
        # print(dB)
        return dB

    @classmethod
    def pole_w_punkcie_caly_odcinek(cls, coordsdB, cable_coords: np.array):
        db_sum = np.array([0, 0, 0])
        for i in range(cable_coords.shape[0]-1):
            db = PoleMagnetyczne.pole_w_punkcie_odcinek(coordsdB,100, cable_coords[i], cable_coords[i+1])
            db_sum = db_sum + db
            # print(db)
        return db_sum

