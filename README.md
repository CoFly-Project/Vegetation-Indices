<p align="center">
<img src="https://user-images.githubusercontent.com/77329407/105342573-3040e900-5be9-11eb-92df-7c09392b1e0c.png" width="300" />
  
# Vegetation Indices

This module extracts 4 different RGB-based vegetation indices from a given input image. The calculated indices are:
1. VARI
2. GLI
3. NGRDI
4. NGBDI


## How to run
```
python3 index_calculation.py ~IMAGE_PATH ~OUTPUT_PATH
```
The ```~IMAGE_PATH``` refers to the absolute path of the input image and the ```~OUTPUT_PATH``` to the absolute path of the preferred folder where the extracted results of the vegetation indices and their corresponding ```*.npy``` files will be saved. 
  
> Note: The ```*.npy``` files are necessary for the calculation of the ```Problematic-Areas-Detection``` module.
  
  
## Dependencies 
Install all the neccecary dependencies using ```pip3 install <package name>```
  
Required packages:
  * numpy   
  * matplotlib 
  * opencv-python
  * pillow 

  
## Results
Example of the ```Vegetation Index``` module results
  <tr class="center">
    <td><img src= =500x500 /></td>
    <td><img src= =500x500 /></td>
    <td><img src= =500x500/></td>    
  </tr>
  
  <img src="https://user-images.githubusercontent.com/26482319/114688051-021d0200-9d1d-11eb-9e08-3b921a7384ee.jpg"/>
  <img src="https://user-images.githubusercontent.com/26482319/114688051-021d0200-9d1d-11eb-9e08-3b921a7384ee.jpg"/>

## Citation
(not published yet)



