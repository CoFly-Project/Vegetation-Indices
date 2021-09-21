import os
import numpy as np
import cv2
import matplotlib.pyplot as plt


class Indexes:
    def __init__(self, img):
        self.img = img
        # self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        self.R = self.img[:, :, 2].astype(np.float32)
        self.G = self.img[:, :, 1].astype(np.float32)
        self.B = self.img[:, :, 0].astype(np.float32)

    def VARI(self):
        vari = np.divide((self.G - self.R), (self.G + self.R - self.B + 0.00001))
        return np.clip(vari, -1, 1)

    def GLI(self):
        gli = np.divide((2 * self.G - self.R - self.B), (2 * self.G + self.R + self.B + 0.00001))
        return np.clip(gli, -1, 1)

    def Visual_NDVI(self):  # Normalized green red difference index
        v_ndvi = np.divide((self.G - self.R), (self.G + self.R + 0.00001))
        return np.clip(v_ndvi, -1, 1)

    def NGBDI(self):
        ngbdi = (self.G - self.B) / (self.G + self.B + 0.00001)
        ngbdi = np.clip(ngbdi, -1, +1)
        return ngbdi

    def get_index(self, index_name):
        if index_name == 'vari':
            return self.VARI()
        elif index_name == 'gli':
            return self.GLI()
        elif index_name == 'vndvi':
            return self.Visual_NDVI()
        elif index_name == 'ngbdi':
            return self.NGBDI()
        elif index_name == 'tgi':
            return self.TGI()
        else:
            print('Uknown index')


def find_real_min_max(perc, edges, index_clear):
    mask = perc > (0.05 * len(index_clear))
    edges = edges[:-1]
    min_v = edges[mask].min()
    max_v = edges[mask].max()
    return min_v, max_v


img_path = '/home/mikrestenitis/CoFly/Indexes Inspection/real_life_exp/cropped_larisa_july.tif'
img_name = 'larisa_jul'

save_dir = './output/{}'.format(img_name)
os.makedirs(save_dir, exist_ok=True)

img_4ch = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
img = img_4ch[:, :, :3].astype(np.float)
img[img_4ch[:, :, 3] == 0] = np.nan
empty_space = img_4ch[:, :, 3] == 0

print('Processing image wthi shape {} x {}'.format(img.shape[0], img.shape[1]))

# -- Calculate index -- #
Idx = Indexes(img)
index_names = ['vari', 'ngbdi', 'gli', 'vndvi']

for index_name in index_names:
    # -- Calculate index -- #
    index = Idx.get_index(index_name)
    np.save('{}/{}.npy'.format(save_dir, index_name), index)

    # -- Calculate index histogram -- #
    index_clear = index[~np.isnan(index)]
    print('Mean: {}'.format(np.mean(index_clear)))
    print('Median: {}'.format(np.median(index_clear)))

    plt.figure()
    perc, edges, _ = plt.hist(index_clear, bins=100, range=(-1, 1), color='darkcyan', edgecolor='black')
    plt.title("Histogram")
    plt.xlim(-1, 1)
    plt.savefig('{}/{}_hist.png'.format(save_dir, index_name), pad_inches=0)
    plt.close()

    # -- Plot index (-1, 1) -- #
    plt.figure()
    plt.imshow(index, cmap="RdYlGn", vmin=-1, vmax=1)
    plt.colorbar()
    plt.savefig('{}/{}_-1_1.png'.format(save_dir, index_name), pad_inches=0)
    plt.close()

    # -- Plot index (min, max) -- #
    lower, upper = find_real_min_max(perc, edges, index_clear)
    print('Min: {}'.format(lower))
    print('Max: {}'.format(upper))
    plt.figure()
    plt.imshow(np.clip(index, lower, upper), cmap="RdYlGn")
    plt.colorbar()
    plt.savefig('{}/{}_min_max.png'.format(save_dir, index_name), pad_inches=0)
    plt.close()

    index_clipped = np.clip(index, lower, upper)
    np.save('{}/{}_clipped.npy'.format(save_dir, index_name), index_clipped)
