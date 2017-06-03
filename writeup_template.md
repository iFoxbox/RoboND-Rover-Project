## Project: Search and Sample Return

---


**The goals / steps of this project are the following:**  

[//]: # (Image References)

[image1]: ./misc/rover_image.jpg
[image2]: ./calibration_images/example_grid1.jpg
[image3]: ./calibration_images/example_rock1.jpg 
[image4]: ./output/warped_ubs1.jpg
[image5]: ./output/warped_ubs2.jpg
[image6]: ./output/rock_found.jpg

## [Rubric](https://review.udacity.com/#!/rubrics/916/view) Points
### Here I will consider the rubric points individually and describe how I addressed each point in my implementation.  

---
### Writeup / README

#### 1. Modified the template writeup and added the points addressed in the rubric. 

### Notebook Analysis
#### 1. Run the functions provided in the notebook on test images (first with the test data provided, next on data you have recorded). Add/modify functions to allow for color selection of obstacles and rock samples.
The first task in the notebook analysis was to write code for detecting a rock sample and an ubstruction or terrain that cannot be navigated. 
I preformed my analysis on the following image. I choose this capture to perform all three tests on the same image. 

![alt text][image3]

I first created the find_ubstruction() function to take the image given and find any terrain that could not be driven on. 
This function was created to be like color_thresh(), but instead of masking the dark spectrum of RGB it masked the lighter side. 
This provided me with the following mask.
![alt text][image4]

I then created highlight_rock(). This function creates a threshold highlighting the gold of the rock samples by masking out any RGB values not to be in the "goldish" color range. 
I found a good upper limit to be (255,255,75) and a lower limit of (100,100,0). The result is seen below. 
![alt text][image6]

After working on the project for a time I found that my fidelity was low. I guessed some of it was because of how my find_ubstruction() was being handled. 
I redesigned it to re_find_ubstruction() which has an upper and lower limit like highlight_rock(). This allowed me to get rid of the pixels it thought was unnavigable that was to the left and right.
![alt text][image5]

#### 1. Populate the `process_image()` function with the appropriate analysis steps to map pixels identifying navigable terrain, obstacles and rock samples into a world map.  Run `process_image()` on your test data using the `moviepy` functions provided to create video output of your result. 
To fill in the process_image() function I followed the provided steps. 
i. Defined a forward-facing source reference point on our image and the top down source equivalent. 
ii. Created a warped top down image given the front facing image. 
iii. Applied the three different thresholds to terrain, obstacles, and rocks in the given warped image. 
iv. Calculated the pixel locations of the three different thresholder images in reference to the rovers location. 
v. Converted the above pixel locations to be in reference to the whole mappable area. 
vi. Updated these values to the data class. 
vii. Created an image mosaic that was then put into the video. 

### Autonomous Navigation and Mapping

#### 1. Fill in the `perception_step()` (at the bottom of the `perception.py` script) and `decision_step()` (in `decision.py`) functions in the autonomous mapping scripts and an explanation is provided in the writeup of how and why these functions were modified as they were.
i. The perception_step() was filled in similarly to process_image() in the test notebook. The function takes a Rover() class that is updated regularly with info from the rover. 
This contains images and telemetry data used for processing the rover's environment. The navigation angels are updated in this step. This determines the best direction for travel by taking the average of all navigable terrain. 
Two addition was made here in comparison to process_image(). I masked the warped thresholded images. I did this at 4 meters. I did this increase accuracy of the images that were being sent to maps. 
I also added a case where the map would not update the map with the current data being passed to it. I found that when you only add images to the map pitch and roll of +- 1.5 degrees from 0 degrees the map would be more accurate. 

ii. The decision_step() I kept very similar to the example code that was give. I modified it by adding a reusable function to call stops.
In the forward mode the rover will travel in the direction of most navigable terrain shown by the thresholded images. 
If the number of pixels starts to drop off and reach a minimum the rover will trigger a stop and start to turn left untill more terrain is seen. 
If the Rover happens to stop in front of a rock sample it will attempt to pick it up.

#### 2. Launching in autonomous mode your rover can navigate and map autonomously.  Explain your results and how you might improve them in your writeup.  
After making the changes to perception.py I found that the rover was able to map the terrain with a fidelity 75% consistently. 
I could improve this by making the perspective transform take account for pitch and roll. I could improve the decision.py 
by adding a feature to tell how close to a wall it has seen and try to stay close to it. Mapping the closed perimeter of the map. 

**Simulator settings (resolution and graphics quality set on launch) and frames per second (FPS output to terminal by `drive_rover.py`) in your writeup when you submit the project so your reviewer can reproduce your results.**
I am running the Roversim at a resolution of 1152 x 864. Graphics quality is set to Fantastic. The FPS I am getting is 30-39 FPS. 
Here I'll talk about the approach I took, what techniques I used, what worked and why, where the pipeline might fail and how I might improve it if I were going to pursue this project further.  



![alt text][image3]


