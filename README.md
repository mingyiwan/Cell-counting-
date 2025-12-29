# Cell-counting
This is the python scripts that allows counting signal colocalizations when used in combination with ImageJ. The script is developed by Mingyi Wan at UCLA Catherine Cahill Lab.
Instructions:
1. Before running the cell counting program, make sure to arrange the ROI files in the following way. It is the important to keep the order of the ROI zip files correct, especially keep the DAPI channel to the last, as the program is coded to recognize the last file in the folder as the DAPI channel. 
  ->Master folder
    ->Folder for animal 1
       ->ROI zip file for channel 1
       ->ROI zip file for channel 2
       ->ROI zip file for channel 3
       ->ROI zip file for DAPI
   ->Folder for animal 2
       ->ROI zip file for channel 1
       ->ROI zip file for channel 2
       ->ROI zip file for channel 3
       ->ROI zip file for DAPI
   ...
   ->Folder for animal n
       ->ROI zip file for channel 1
       ->ROI zip file for channel 2
       ->ROI zip file for channel 3
       ->ROI zip file for DAPI
   
    
2. Run Function.py before running cell counting.py
3. Changes you can/need to make in the cell counting.py:
    1.[Need to make] Put in the location of the master folder in line 25
    2. You can change the name and location of the output result file in line 127
    3. You can change the number of channels from line 37-40
    4. You can change the output column name of your channels from line 113-123
4. Run cell counting.py
