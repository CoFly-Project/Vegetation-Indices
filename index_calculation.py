import os
import numpy as np
import cv2
import matplotlib.pyplot as plt
import sys


# -- Create a class for calculating the vegetation_index -- #
class Indexes:
	def __init__(self, img):
		self.img = img
		self.R = self.img[:, :, 2].astype(np.float32)
		self.G = self.img[:, :, 1].astype(np.float32)
		self.B = self.img[:, :, 0].astype(np.float32)


	# All these operations aim to not have ZeroDivisionError -- #
	# -- Visible Atmospheric Resistant Index -- #
	def VARI(self):
		vari = np.divide((self.G - self.R), (self.G + self.R - self.B + 0.00001))
		return np.clip(vari, -1, 1) # -- VI values outside the [-1, 1] are clipped to this interval edges. -- #

	# -- Green Leaf Index -- #
	def GLI(self):
		gli = np.divide((2 * self.G - self.R - self.B), (2 * self.G + self.R + self.B + 0.00001))
		return np.clip(gli, -1, 1)

	# -- Normalized Green Red Difference Index -- #
	def NGRDI(self):  
		v_ndvi = np.divide((self.G - self.R), (self.G + self.R + 0.00001))
		return np.clip(v_ndvi, -1, 1)

	# -- Normalized Green Blue Difference Index -- #
	def NGBDI(self): 
		ngbdi = (self.G - self.B) / (self.G + self.B + 0.00001)
		ngbdi = np.clip(ngbdi, -1, +1)
		return ngbdi

	# --  Identification of the Idx object -- #
	def get_index(self, index_name):
		if index_name == 'VARI':
			return self.VARI()
		elif index_name == 'GLI':
			return self.GLI()
		elif index_name == 'NGRDI':
			return self.NGRDI()
		elif index_name == 'NGBDI':
			return self.NGBDI()
		else:
			print('Uknown index')


# -- Find the real values of the min, max based on the frequency of the vegetation_index histogramm' s bin in each examined interval -- #
def find_real_min_max(perc, edges, index_clear):
	mask = perc > (0.05 * len(index_clear))
	edges = edges[:-1]
	min_v = edges[mask].min()
	max_v = edges[mask].max()
	return min_v, max_v

# -- A necessary message for the arguments
parser = argparse.ArgumentParser(epilog = textwrap.dedent('''\
						        The available VIs are:
						        1. Visible Atmospheric Resistant Index (VARI)
						        2. Green Leaf Index (GLI)
						        3. Normalized Green Red Difference Index (NGRDI)
						        4. Normalized Green Blue Difference Index (NGBDI)
						        '''), formatter_class=argparse.RawTextHelpFormatter)

# -- Parsing the args -- #
parser.add_argument('--input_image', required=True,
			  help="Please enter the absolute path of the input image.")

parser.add_argument('--output_path', required=True,
			  help="Please enter the absolute path of the output path.")

parser.add_argument('--vis', nargs = '*',
			  help="Please enter the short name of the vegetation index/indices.")

args = parser.parse_args()

img_path = os.path.abspath(args.input_image)
img_name = os.path.basename(img_path)
save_dir = os.path.abspath(args.output_path)
index = args.vis

# -- Check for the arguments if they are None -- #
if index == None:
	index = ['VARI', 'GLI', 'NGRDI', 'NGBDI']

index  = [elem.upper() for elem in index]

img_4ch = cv2.imread(img_name, cv2.IMREAD_UNCHANGED)
img = img_4ch[:, :, :3].astype(np.float)
img[img_4ch[:, :, 3] == 0] = np.nan
empty_space = img_4ch[:, :, 3] == 0

# -- Print function for testing reasons -- #
print('Processing image with shape {} x {}'.format(img.shape[0], img.shape[1]))


Idx = Indexes(img)

for i in index:
	# -- Calculate index -- #
	idx = Idx.get_index(i)


	index_clear = idx[~np.isnan(idx)]

	# -- Calculate index histogram -- #
	perc, edges, _ = plt.hist(index_clear, bins=100, range=(-1, 1), color='darkcyan', edgecolor='black')

	# -- Find the real min, max values of the vegetation_index -- #
	lower, upper = find_real_min_max(perc, edges, index_clear)

	# -- Plot and save the vegetation_index -- #
	f = plt.figure()
	f.set_figheight(idx.shape[0]/f.get_dpi())
	f.set_figwidth(idx.shape[1]/f.get_dpi())
	ax = plt.Axes(f, [0., 0., 1., 1.])
	ax.set_axis_off()
	f.add_axes(ax)
	ax.imshow(np.clip(idx, lower, upper), cmap='RdYlGn', aspect='auto')
	f.savefig('{}/{}.png'.format(save_dir, i), transparent=True)
	plt.close()

	# -- The *.npy files are useful for the Problematic Areas Detection module -- # 
	index_clipped = np.clip(idx, lower, upper)
	np.save('{}/{}_clipped.npy'.format(save_dir, i), index_clipped)

# -- Print function for testing reasons -- #	
print('Done!')
