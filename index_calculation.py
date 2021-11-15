import os
import numpy as np
import cv2
import matplotlib.pyplot as plt
import sys
import textwrap
from PIL import Image
import matplotlib as mpl
from osgeo import gdal, osr

class Indexes:
	def __init__(self, img):
		self.img = img
		self.R = self.img[:, :, 2].astype(np.float32)
		self.G = self.img[:, :, 1].astype(np.float32)
		self.B = self.img[:, :, 0].astype(np.float32)


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

	def NGBDI(self): 
		ngbdi = (self.G - self.B) / (self.G + self.B + 0.00001)
		return np.clip(ngbdi, -1, +1)

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

def find_real_min_max(perc, edges, index_clear):
	mask = perc > (0.05 * len(index_clear))
	edges = edges[:-1]
	min_v = edges[mask].min()
	max_v = edges[mask].max()
	return min_v, max_v

def array_to_raster(output_path, ds_reference, array, name):
	gdal.AllRegister()
	ds_ref = gdal.Open(ds_reference, gdal.GA_ReadOnly)

	rows, cols, band_num = array.shape

	driver = gdal.GetDriverByName("GTiff")

	outRaster = driver.Create(os.path.join(output_path, name+'.tif'), cols, rows, band_num, gdal.GDT_Float32, options=["COMPRESS=DEFLATE"])
	originX, pixelWidth, b, originY, d, pixelHeight = ds_ref.GetGeoTransform()
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
		else:
			outRaster.GetRasterBand(5).SetColorInterpretation(gdal.GCI_Undefined)
		
	prj = ds_ref.GetProjection()
	outRasterSRS = osr.SpatialReference(wkt=prj)
	outRaster.SetProjection(outRasterSRS.ExportToWkt())
	driver = None
	outband.FlushCache()

	return outRaster
		
		
def winapi_path(dos_path, encoding=None):
    if (not isinstance(dos_path, str) and encoding is not None): 
        dos_path = dos_path.decode(encoding)
    path = os.path.abspath(dos_path)
    if path.startswith(u"\\\\"):
        return u"\\\\?\\UNC\\" + path[2:]
    return u"\\\\?\\" + path


img_path = winapi_path(sys.argv[1])
path_1, path_2 = img_path.split('\\docker_stitching\\')
project_name = path_2.split('\\')[0]
save_dir = winapi_path(os.path.join(sys.argv[2], project_name))
os.makedirs(save_dir, exist_ok=True)

os.chdir(save_dir)
img_4ch = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
img = img_4ch[:, :, :3].astype(float)
img[img_4ch[:, :, 3] == 0] = np.nan
empty_space = img_4ch[:, :, 3] == 0

print('Processing image with shape {} x {}'.format(img.shape[0], img.shape[1]))

indices_names = ['VARI', 'GLI', 'NGRDI', 'NGBDI']
Idx = Indexes(img)

for index_name in indices_names:
	idx = Idx.get_index(index_name)

	index_clear = idx[~np.isnan(idx)]

	perc, edges, _ = plt.hist(index_clear, bins=100, range=(-1, 1), color='darkcyan', edgecolor='black')
	plt.close()

	lower, upper = find_real_min_max(perc, edges, index_clear)
	index_clipped = np.clip(idx, lower, upper)
		
	cm = plt.get_cmap('RdYlGn')
	norm = plt.Normalize(0, 1)
	cNorm = mpl.colors.Normalize(vmax=upper, vmin=lower)
	colored_image = cm(cNorm(index_clipped))
	img = Image.fromarray(np.uint8(colored_image * 255), mode='RGBA')

	rgba = np.array(img, dtype=np.float32)

	array_5ch = np.dstack((rgba, index_clipped))
	array_to_raster(save_dir, img_path, array_5ch, index_name)
	
print('Done!')
