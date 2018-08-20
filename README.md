                            Tracking Mario in Video  
 
 
Goal: Find and track object (Mario) in video using open CV (Template Matching). 
What does this program do? 
Loads an input video and a images patch (templates). 
Perform a template matching procedure by using the Open CV function matchTemplate . 
Localize the location with higher matching probability. 
Draw a rectangle around the area corresponding to the highest match. 
Save the result in another video. 
===================================
        1- Loads an input video and a images patch (templates). 
          Video : https://www.youtube.com/watch?v=Bx6J-Xtps94 
     Read video and templets  
           Cap = cv2.VideoCapture('mario.mkv') 
     mini_mario = cv2.imread('mini_mario.png') 
     big_mario  = cv2.imread('big_mario.png') 
     fire_mario = cv2.imread('fire_mario.png') 
                                         
 
 ![big_mario](https://user-images.githubusercontent.com/35124840/44327056-deb33380-a45d-11e8-9f11-42d47ffb5803.png) 
 
 
 
Read Frame from video and using as input image 
     while True: 
            success, frame = cap.read() 
    
2- Perform a template matching procedure by using the  
Open CV function (matchTemplate ). 
We need two primary components: 
      Source image (I): The image in which we expect to find a match to the template image 
      Template image (T): The patch image which will be compared to the template image 
  our goal is to detect the highest matching area: 
 
 
  +   =     
       Use the OpenCV function matchTemplate to search for matches between an image patch and an input image  
             method=CV_TM_CCOEFF_NORMED 
 
 
 
         Using the OpenCV function minMaxLoc to find the maximum and minimum values (as well as their positions) in a given array. 
     Python: cv2.minMaxLoc(src[, mask]) → minVal, maxVal, minLoc, maxLoc 
         
 
 

Apply this functions on 3 templets and every frame on video. 
res1 = cv2.matchTemplate(frame, mini_mario, cv2.TM_CCOEFF_NORMED) 
min_val1, max_val1, min_loc1, max_loc1 = cv2.minMaxLoc(res1) 
 
res2 = cv2.matchTemplate(frame, big_mario, cv2.TM_CCOEFF_NORMED) 
min_val2, max_val2, min_loc2, max_loc2 = cv2.minMaxLoc(res2) 
 
res3 = cv2.matchTemplate(frame, fire_mario, cv2.TM_CCOEFF_NORMED) 
min_val3, max_val3, min_loc3, max_loc3 = cv2.minMaxLoc(res3) 
 
Based on the max matching calculate in (max_val) 
will draw rectangle on the object . 
3- Draw a rectangle around the area corresponding to  
the highest match. 
top_left = max_loc1 
bottom_right = (top_left[0] + w_mini_mario, top_left[1]  
+ h_mini_mario) 
cv2.rectangle(frame, top_left, bottom_right, 200, 3) 
 
4- Save the result in another video 
out = cv2.VideoWriter('Tracking_mario.avi', cv2.VideoWriter_fourcc(*'DIVX'), 30, size) 
out.write(frame) 
Result: 
 
 






 
 
The Result video : https://www.youtube.com/watch?v=wNnLa7jSK14&t=3s
       🙁 🙁    But his happiness was not complete    🙁 🙁  
The Problem :  
1- when the frame does not contain Mario the  rectangle still appear. 
 
2- when the background is brown in case big Mario the operation fail. 
 
3- when the Mario is (fire Mario) the operation sometimes fail and appear the rectangle on the white object. 

 
 

4- the time taken to produce the output video (very large) about  1 hours 15 minutes. 
 







Analysis the problem: 
   problem 
    expected reasons 
    expected solutions 
 
when the frame does not contain Mario the  rectangle still appear. 
I- Different templates and difficulties of tuning and identification The percentage that determines draw rectangle. 
I- Try and error until reached to the nearest correct ratio to determine the draw rectangle.    
when the background is brown in case big Mario the operation fail 
I- Color convergence between big Mario and background cased in not appear Mario.  
I- Can increase the number of templates to include different case .
when the Mario is (fire Mario) the operation sometimes fail and appear the rectangle on the white object.
I- Ratio white color in fire Mario conflict with white objects in match operation. 
I- Can increase the number of templates to include different case .
the time taken to produce the output video (very large) about  1 hours 15 minutes.
I- High resolution of video in operations (read- write).  
ii- Search operation to find max matching. 
I- Cutting the image to 4 part and search in every part about matching. 
2-Convert image from RGB to Gray scale. 
 

Time:   

Using Function timeit.default_timer() 
Returns the current time instant, a floating-point number of seconds since the epoch. 

Type 
Average time every frame ( seconds) 
Read 
0.00629
Write 
0.01448
Matching 
2.48379
Drawing 
0.01380

Profiling:        

information 
 video 
Resolution 
1920 x 1080 
memory 
31.7 MB 
length 
1 minute 58 seconds 
Frame rate 
30 frames per second 
Total Frame in video 
3537 fame 



 information 
Computer  
Processor 
Up to 8th Gen Intel® Core™ i7 Processor 
Graphics 
 - Intel Integrated Graphics 
- NVIDIA® GeForce® 940MX (4 GB) 
Memory Ram 
16 GB 


