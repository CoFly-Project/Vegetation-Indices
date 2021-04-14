import os
import numpy as np

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

	def Visual_NDVI(self): # Normalized green red difference index
		v_ndvi = np.divide((self.G - self.R), (self.G + self.R + 0.00001))
		return np.clip(v_ndvi, -1, 1)

	def NGBDI(self):
		ngbdi = (self.G - self.B) / (self.G + self.B + 0.00001)
		ngbdi = np.clip(ngbdi, -1, +1)
		return ngbdi
