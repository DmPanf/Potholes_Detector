## 🚀 YOLOv8 Dataset Preparation Guide

Welcome to the YOLOv8 Dataset Preparation Guide! This README provides step-by-step instructions for preparing a new dataset for training with the YOLOv8 model, following the annotation process of the video files! 🌊

### Step 1: Split Video into Frames 🖼️

After annotating all video files, the first step is to split these videos into individual frames. 

**Requirements:**
- Python
- OpenCV library (`opencv-python`)

**Instructions:**
1. Install OpenCV if not already installed:
   ```bash
   pip install opencv-python
   ```

2. Use the provided Python script to split videos into frames. The script will save each frame as a PNG file in a specified directory.

### Step 2: Rename Files (Optional) 🏷️

If required, rename the frames for consistency.

**Instructions:**
1. Use the Bash script in the terminal to rename files in desired format.

### Step 3: Remove Odd Frames 🗑️

To balance or reduce the dataset, you might want to remove odd-numbered frames.

**Instructions:**
1. Run the provided Python script to delete all odd-numbered image files from the images directory.

### Step 4: Sync Labels with Images 🔄

Ensure that each image in the dataset has a corresponding label file.

**Instructions:**
1. Use the Python script to check all files in the `labels` folder and delete those without a corresponding image file in the `images` folder.

### Step 5: Split Dataset into Train and Validation Sets 🚂🔄

Divide your dataset into training (90%) and validation (10%) sets.

**Instructions:**
1. Run the Python script to automatically split all images and labels into `train` and `val` directories, ensuring a random and fair distribution.

### Step 6: Final Checks and Backup 🔍💾

Before proceeding with training:
1. Double-check the dataset for any inconsistencies.
2. Make sure to backup the dataset.

### Conclusion and Next Steps 🎯

Thus we have successfully prepared dataset for training with YOLOv8. 🎉

Next steps include setting up YOLOv8 training environment and starting the training process! 🤖💪
