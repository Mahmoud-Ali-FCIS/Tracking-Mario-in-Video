                             
# Tracking Mario in Video
                                               
 
## Goal: Find and track object (Mario) in video using open CV (Template Matching). 

What does this program do? 

   1. Loads an input video and a images patch (templates). 

   2. Perform a template matching procedure by using the Open CV function matchTemplate . 

   3. Localize the location with higher matching probability.

   4. Draw a rectangle around the area corresponding to the highest match.

   5. Save the result in another video. 

### start processes ###

**1. Loads an input video and a images patch (templates).**
        
   Video : https://www.youtube.com/watch?v=Bx6J-Xtps94 
          
   - Read video and templets  
   ```
      Cap = cv2.VideoCapture('mario.mkv')    
     
      mini_mario = cv2.imread('mini_mario.png')
     
      big_mario  = cv2.imread('big_mario.png') 
     
      fire_mario = cv2.imread('fire_mario.png') 
   ```

 ![mini_mario](https://user-images.githubusercontent.com/35124840/44330020-41a8c880-a466-11e8-818b-ee0368da13e1.png)
 ![big_mario](https://user-images.githubusercontent.com/35124840/44327056-deb33380-a45d-11e8-9f11-42d47ffb5803.png) 
 ![fire_mario](https://user-images.githubusercontent.com/35124840/44330023-44a3b900-a466-11e8-8832-a3d266415bb7.png)
 
 
 
   - Read Frame from video and using as input image 
   ```
   while True: 
   
         success, frame = cap.read() 
   ```        
**2. Perform a template matching procedure by using the Open CV function (matchTemplate ).** 

   - We need two primary components: 

        **Source image (I):** The image in which we expect to find a match to the template image 
      
        **Template image (T):** The patch image which will be compared to the template image 
      
   **our goal is to detect the highest matching area** 
 
 
 ![screenshot from 2018-08-07 19-17-42](https://user-images.githubusercontent.com/35124840/44330230-c1cf2e00-a466-11e8-9c6e-d9f5f5d9e10b.png) + ![big_mario](https://user-images.githubusercontent.com/35124840/44327056-deb33380-a45d-11e8-9f11-42d47ffb5803.png)   =    
 ![screenshot from 2018-08-07 19-15-29](https://user-images.githubusercontent.com/35124840/44330232-c4318800-a466-11e8-9209-2876e90b06ff.png)
  
   - Use the OpenCV function matchTemplate to search for matches between an image patch and an input image  
       
   **method=CV_TM_CCOEFF_NORMED**
             
   ![235e42ec68d2d773899efcf0a4a9d35a7afedb64](https://user-images.githubusercontent.com/35124840/44330477-66517000-a467-11e8-8d1f-461c745d5f8a.png)
 
 
 
   - Using the OpenCV function minMaxLoc to find the maximum and minimum values (as well as their positions) in a given array. 
         
     **Python: cv2.minMaxLoc(src[, mask]) → minVal, maxVal, minLoc, maxLoc** 
         

     - Apply this functions on 3 templets and every frame on video. 

     ```
     res1 = cv2.matchTemplate(frame, mini_mario, cv2.TM_CCOEFF_NORMED)

     min_val1, max_val1, min_loc1, max_loc1 = cv2.minMaxLoc(res1) 

                     
     res2 = cv2.matchTemplate(frame, big_mario, cv2.TM_CCOEFF_NORMED) 

     min_val2, max_val2, min_loc2, max_loc2 = cv2.minMaxLoc(res2) 

                     
     res3 = cv2.matchTemplate(frame, fire_mario, cv2.TM_CCOEFF_NORMED) 

     min_val3, max_val3, min_loc3, max_loc3 = cv2.minMaxLoc(res3) 
     ```

     Based on the max matching calculate in (max_val) 

     will draw rectangle on the object . 

**3. Draw a rectangle around the area corresponding to the highest match.**
```
    top_left = max_loc1 

    bottom_right = (top_left[0] + w_mini_mario, top_left[1] + h_mini_mario) 

    cv2.rectangle(frame, top_left, bottom_right, 200, 3) 
```

![screenshot from 2018-08-07 19-15-29](https://user-images.githubusercontent.com/35124840/44330232-c4318800-a466-11e8-9209-2876e90b06ff.png)
 
**4. Save the result in another video** 
```
    out = cv2.VideoWriter('Tracking_mario.avi', cv2.VideoWriter_fourcc(*'DIVX'), 30, size) 

    out.write(frame) 
```


### Result: 

 
 ![screenshot from 2018-08-07 20-05-08](https://user-images.githubusercontent.com/35124840/44329626-32754b00-a465-11e8-9a27-570137799e39.png)
![screenshot from 2018-08-07 20-08-26](https://user-images.githubusercontent.com/35124840/44329631-3739ff00-a465-11e8-9512-850168f50b56.png)
![screenshot from 2018-08-07 20-06-18](https://user-images.githubusercontent.com/35124840/44329640-3ef9a380-a465-11e8-86ea-9a911e80117f.png)
![screenshot from 2018-08-07 20-08-49](https://user-images.githubusercontent.com/35124840/44329672-4f118300-a465-11e8-966f-618958c5a815.png)
![screenshot from 2018-08-07 20-09-46](https://user-images.githubusercontent.com/35124840/44329697-5e90cc00-a465-11e8-992b-3f8c4c30471b.png)
![screenshot from 2018-08-07 20-10-29](https://user-images.githubusercontent.com/35124840/44329704-6486ad00-a465-11e8-8a2a-120e548ea5ec.png)


### The Result video : https://www.youtube.com/watch?v=wNnLa7jSK14&t=3s


                               🙁 🙁    But his happiness was not complete    🙁 🙁  
       
### The Problem :  

**1. when the frame does not contain Mario the  rectangle still appear.**
 ![screenshot from 2018-08-07 20-08-18](https://user-images.githubusercontent.com/35124840/44329391-9c412500-a464-11e8-8e86-9798d413a4b8.png)
**2. when the background is brown in case big Mario the operation fail.**
 ![screenshot from 2018-08-07 20-07-57](https://user-images.githubusercontent.com/35124840/44329368-92b7bd00-a464-11e8-81ed-29effad7e60f.png)
**3. when the Mario is (fire Mario) the operation sometimes fail and appear the rectangle on the white object.** 
 ![screenshot from 2018-08-07 20-08-18](https://user-images.githubusercontent.com/35124840/44329391-9c412500-a464-11e8-8e86-9798d413a4b8.png)
 
**4. the time taken to produce the output video (very large) about  2 hours 11 minutes.** 
 

### Analysis the problem: 
     
     
| **problem**      | **expected reasons**  | **expected solutions** |
| :---         |       :---:       |               ---: |
| when the frame does not contain Mario the  rectangle still appear| I- Different templates and difficulties of tuning and identification The percentage that determines draw rectangle| I- Try and error until reached to the nearest correct ratio to determine the draw rectangle|
| when the background is brown in case big Mario the operation fail| I- Color convergence between big Mario and background cased in not appear Mario.| I- Can increase the number of templates to include different case. II- Reduce size of frame and search area by cutting the size of next frame based on the area which surround to the position of Mario in current frame.|
| when the Mario is (fire Mario) the operation sometimes fail and appear the rectangle on the white object|I- Ratio white color in fire Mario conflict with white objects in match operation|I- Can increase the number of templates to include different case. II- Reduce size of frame and search area by cutting the size of next frame based on the area which surround to the position of Mario in current frame.|
| the time taken to produce the output video (very large) about  2 hours 11 minutes|I- High resolution of video in operations (read- write).  II- Search operation to find max matching|I- Cutting the image to 4 part and search in every part about matching.  II-Convert image from RGB to Gray scale. III-Convert code from sequential to parallel by using multi-threading.|


### Time:   

- Using Function timeit.default_timer() 
  Returns the current time instant, a floating-point number of seconds since the epoch. 

|  **Type** | **Average time every frame ( seconds)**   |
| --- | --- |
| Read | 0.00629 |
| Write | 0.01448 | 
| Matching|2.48379  |
| Drawing|0.01380 |

 
### Profiling:        


|  **information** | **video**  |
| --- | --- |
| Resolution | 1920 x 1080  |
| memory | 31.7 MB |
| length| 1 minute 58 seconds  |
| Frame rate | 30 frames per second  |
| Total Frame in video| 3537 fame  |



|  **information** | **Computer** |
| --- | --- |
| Processor | Up to 8th Gen Intel® Core™ i7 Processor  |
| Graphics |  - Intel Integrated Graphics - NVIDIA® GeForce® 940MX (4 GB) |
| Memory Ram | 16 GB |

  
 
 
 
 



