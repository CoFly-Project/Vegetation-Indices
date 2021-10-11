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
  
  
<!-- ![vari](https://user-images.githubusercontent.com/80779522/136771613-e153e5e7-4f81-4ff0-9832-667e636e1c4a.png)
![ngrdi](https://user-images.githubusercontent.com/80779522/136771653-e6b77f42-789f-4100-86ac-68ff013a55ba.png)
![gli](https://user-images.githubusercontent.com/80779522/136771662-00ad0db0-3057-4223-97f2-2a10ff52c602.png)
![ngbdi](https://user-images.githubusercontent.com/80779522/136771673-89c7463d-387d-4c36-a18c-2764fbb1ab1e.png) -->
  

<!-- <img src= "https://user-images.githubusercontent.com/80779522/136773402-d76cdbea-143c-42e4-9df9-10ec277c902a.png" =100x100 /> -->
<!--   <tr align="center">
    <td>(a) Input image</td>
  </tr> -->

  
<table class="center">
   <tr class="center">
    <td><img src= "https://user-images.githubusercontent.com/80779522/136773402-d76cdbea-143c-42e4-9df9-10ec277c902a.png" =400x400 /></td>
    <td><img src= "https://user-images.githubusercontent.com/80779522/136771613-e153e5e7-4f81-4ff0-9832-667e636e1c4a.png" =400x400 /></td>
    <td><img src= "https://user-images.githubusercontent.com/80779522/136771662-00ad0db0-3057-4223-97f2-2a10ff52c602.png" =400x400 /></td>   
   </tr>   
   <tr align="center">
    <td>(a) Input image</td>
    <td>(b) VARI</td>
    <td>(c) GLI</td>    
 
  </tr>  
  <tr class="center">
    <td><img src= "https://user-images.githubusercontent.com/80779522/136771653-e6b77f42-789f-4100-86ac-68ff013a55ba.png" =400x400 /></td>
    <td><img src= "https://user-images.githubusercontent.com/80779522/136771673-89c7463d-387d-4c36-a18c-2764fbb1ab1e.png" =400x400 /></td>   
  </tr>
  <tr align="center">
    <td>(d) NGRDI</td>
    <td>(e) NGBDI</td>
  </tr>

</table>

  **Figure 1** Results of the ```Vegetation Indices``` module results: (a) a given RGB input image, (b) VARI, (c) GLI, (d) NGRDI and (e) NGBDI.
  
## Citation
(not published yet)



