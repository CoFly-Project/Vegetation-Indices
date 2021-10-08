import os
import numpy as np
import cv2
import matplotlib.pyplot as plt
import sys
from PIL import Image
import glob


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

	def NGRDI(self):  # Normalized green red difference index
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
		elif index_name == 'ngrdi':
			return self.NGRDI()
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


img_path = os.path.abspath(sys.argv[1])
img_name = os.path.basename(img_path)
os.chdir(img_path.split(img_name)[0])

img_4ch = cv2.imread(img_name, cv2.IMREAD_UNCHANGED)
img = img_4ch[:, :, :3].astype(np.float)
img[img_4ch[:, :, 3] == 0] = np.nan
empty_space = img_4ch[:, :, 3] == 0

print('Processing image with shape {} x {}'.format(img.shape[0], img.shape[1]))


save_dir = os.path.abspath(sys.argv[2])
os.chdir(save_dir)


Idx = Indexes(img)
index_names = ['vari', 'ngbdi', 'gli', 'ngrdi']

for index_name in index_names:
	index = Idx.get_index(index_name)

	index_clear = index[~np.isnan(index)]
	perc, edges, _ = plt.hist(index_clear, bins=100, range=(-1, 1), color='darkcyan', edgecolor='black')
	lower, upper = find_real_min_max(perc, edges, index_clear)

	f = plt.figure()
	f.set_figheight(index.shape[0]/f.get_dpi())
	f.set_figwidth(index.shape[1]/f.get_dpi())
	ax = plt.Axes(f, [0., 0., 1., 1.])
	ax.set_axis_off()
	f.add_axes(ax)
	ax.imshow(np.clip(index, lower, upper), cmap="RdYlGn", aspect='auto')
	f.savefig('{}/{}.png'.format(save_dir, index_name))
	plt.close()

	index_clipped = np.clip(index, lower, upper)
	np.save('{}/{}_clipped.npy'.format(save_dir, index_name), index_clipped)

def transparent(img):
	img = Image.open(img)
	img = img.convert("RGBA")

	pixdata = img.load()

	width, height = img.size
	for y in range(height):
		for x in range(width):
			if pixdata[x, y] == (255, 255, 255, 255):
				pixdata[x, y] = (255, 255, 255, 0)

	img.save(image, "PNG")

for img_path in glob.glob(save_dir):
	for image in glob.glob(os.path.join(img_path, '*.png')):
		transparent(image)

print('Done!')
