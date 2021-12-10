import os
import numpy as np
import cv2
import matplotlib.pyplot as plt
import argparse
import textwrap
from PIL import Image
import matplotlib as mpl
from osgeo import gdal, osr


# -- Create a class for each vegetation_index -- #
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
		return np.clip(ngbdi, -1, +1)

	# -- Identification of the Idx object -- #
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

# -- Function that creates the georeferenced VI map -- #
def array_to_raster(output_path, ds_reference, array, name1, name2):
	rows, cols, band_num = array.shape

	driver = gdal.GetDriverByName("GTiff")

	outRaster = driver.Create(os.path.join(output_path, name1+'_'+name2+'.tif'), cols, rows, band_num, gdal.GDT_Byte, options=["COMPRESS=DEFLATE"])
	originX, pixelWidth, b, originY, d, pixelHeight = ds_reference.GetGeoTransform()
	outRaster.SetGeoTransform((originX, pixelWidth, 0, originY, 0, pixelHeight))

	descriptions = ['Red Band', 'Green Band', 'Blue Band', 'Alpha Band', 'Index Array']
	for b in range(band_num):
		outband = outRaster.GetRasterBand(b+1)
		outband.WriteArray(array[:,:,b])
		outband.SetDescription(descriptions[b])
		if b+1==1:
			outRaster.GetRasterBand(1).SetColorInterpretation(gdal.GCI_RedBand)
		elif b+1==2:
			outRaster.GetRasterBand(2).SetColorInterpretation(gdal.GCI_GreenBand)
		elif b+1==3:
			outRaster.GetRasterBand(3).SetColorInterpretation(gdal.GCI_BlueBand)
		elif b+1==4:
			outRaster.GetRasterBand(4).SetColorInterpretation(gdal.GCI_AlphaBand)
		
	
	outRasterSRS = osr.SpatialReference(wkt=prj)
	outRaster.SetProjection(outRasterSRS.ExportToWkt())
	driver = None
	outband.FlushCache()

	print('Georeferenced {} map was extracted!'.format(index_name))

	return outRaster

# -- Arguments -- #	
parser = argparse.ArgumentParser(prog='index_calculation', description = textwrap.dedent('''\
								The available VIs are:
								1. Visible Atmospheric Resistant Index (VARI)
								2. Green Leaf Index (GLI)
								3. Normalized Green Red Difference Index (NGRDI)
								4. Normalized Green Blue Difference Index (NGBDI)
								'''), formatter_class=argparse.RawTextHelpFormatter)


parser.add_argument('--input_image', required=True, help="Please enter the absolute path of the input image.")
parser.add_argument('--output_path', nargs='?', help="Please enter the absolute path of the output path.")
parser.add_argument('--vis', nargs="*", required=False, help="Please enter the abbreviation of the Vegetation Index/Indices.")
args = parser.parse_args()

if args.output_path==None: 
	os.makedirs('results', exist_ok=True)
	save_dir = os.path.join(os.getcwd(), 'results')
else:
	save_dir = os.path.abspath(args.output_path)

if len(args.vis) == 0:
	args.vis = ['VARI', 'GLI', 'NGRDI', 'NGBDI']
	print('All VIs will be calculated!')
else:
	args.vis = [elem.upper() for elem in args.vis]
	
img_path = os.path.abspath(args.input_image)
img_name = os.path.basename(img_path)
name, ext = os.path.splitext(img_name)

os.chdir(os.path.dirname(img_path))

img = cv2.imread(img_name, cv2.IMREAD_UNCHANGED)
h, w, ch = img.shape

if ch > 3:
	image = img[:, :, :3].astype(float)
	image[img[:, :, 3] == 0] = np.nan
	empty_space = img[:, :, 3] == 0
else:
	image = img

# -- Print function for testing reasons -- #
print('Processing image with shape {} x {}'.format(img.shape[0], img.shape[1]))

Idx = Indexes(image)

for index_name in args.vis:
	# -- Calculate index -- #
	idx = Idx.get_index(index_name)

	index_clear = idx[~np.isnan(idx)]

	# -- Calculate index histogram -- #
	perc, edges, _ = plt.hist(index_clear, bins=100, range=(-1, 1), color='darkcyan', edgecolor='black')
	plt.close()

	# -- Find the real min, max values of the vegetation_index -- #
	lower, upper = find_real_min_max(perc, edges, index_clear)
	index_clipped = np.clip(idx, lower, upper)
	
	cm = plt.get_cmap('RdYlGn')
	cNorm = mpl.colors.Normalize(vmax=upper, vmin=lower)
	colored_image = cm(cNorm(index_clipped))

	img = Image.fromarray(np.uint8(colored_image * 255), mode='RGBA')
	
	rgba = np.array(img, dtype=np.float32)

	ds = gdal.Open(img_path, gdal.GA_ReadOnly)
	prj = ds.GetProjection()

	if prj: 
		array_to_raster(save_dir, ds, rgba, name, index_name)	
	else:
		img.save('{}/{}_{}.tif'.format(save_dir, name, index_name))
		print('Non georeferrenced {} map was extracted!'.format(index_name))

	np.save('{}/{}_{}.npy'.format(save_dir, name, index_name), index_clipped)
	
print('Done!')
