# Dot_count
Counting number of dots on dices
# Algorithm
- Step1: Read input image of dices.
- Step2: Convert image to gray, do Histogram Equalization and apply GaussianBlur.
- Step3: Do Canny for edge detection.
- Step4: FloodFill from point (0,0) of the image to segment out background.
- Step5: Make every blob a mask and crop out that part of the original image.
- Step6: On each crop, call count function from counter.py for dot counting.
- Step7: Show on screen.

# Output
![Alt text](Screen_shot/output.png?raw=true "OUTPUT")

# Tools
- numpy
- opencv
# Source 
Detect_dice.py

