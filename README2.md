# Tracking Mario in Video
                                               
 
## Goal: Solve some of problems which appear in program try Find and track object (Mario) in video using open CV (Template Matching).

### The problems was From the previous document “README”: 



| **problem**      | **expected reasons**  | **expected solutions** |
| :---         |       :---:       |               ---: |
| when the frame does not contain Mario the  rectangle still appear| I- Different templates and difficulties of tuning and identification The percentage that determines draw rectangle| I- Try and error until reached to the nearest correct ratio to determine the draw rectangle|
| when the background is brown in case big Mario the operation fail| I- Color convergence between big Mario and background cased in not appear Mario.| I- Can increase the number of templates to include different case. II- Reduce size of frame and search area by cutting the size of next frame based on the area which surround to the position of Mario in current frame.|
| when the Mario is (fire Mario) the operation sometimes fail and appear the rectangle on the white object|I- Ratio white color in fire Mario conflict with white objects in match operation|I- Can increase the number of templates to include different case. II- Reduce size of frame and search area by cutting the size of next frame based on the area which surround to the position of Mario in current frame.|
| the time taken to produce the output video (very large) about  2 hours 11 minutes|I- High resolution of video in operations (read- write).  II- Search operation to find max matching|I- Cutting the image to 4 part and search in every part about matching.  II-Convert image from RGB to Gray scale. III-Convert code from sequential to parallel by using multi-threading.|

### The main problem was ( problem of time ). 
   - The time taken to produce the output video was  (very large).  

   - It was about (2 hours 11 minutes), it is a huge time and not accepted. 
   
   - Try Solving this problem using: 

      **(1)** Cutting only the interested rejoin from frame which contain on Mario. 

      **(2)** Convert code from sequential to parallel by using multi-threading. 
      
### Solution the problem: 

   - **The first method:** 
   
     **(1)** Cutting only the interested rejoin from frame which contain on Mario.
     
           - search on Mario in the all frame. 

           - if found it in frame  

             - cutting the rejoin of interested and this cutting frame will be the frame which 
               in next time. 

           -if not found it in frame  

             - search in next time in all frame until found it. 
     

   - **1- Search on Mario in the all frame using the Open CV function (matchTemplate ).**  

     - We need two primary components: 

      - **Source image (I):** The image in which we expect to find a match to the template image 
      
      - **Template image (T):** The patch image which will be compared to the template image 
      
   **Goal is to detect the highest matching area** 
 
 
 ![screenshot from 2018-08-07 19-17-42](https://user-images.githubusercontent.com/35124840/44330230-c1cf2e00-a466-11e8-9c6e-d9f5f5d9e10b.png) + ![big_mario](https://user-images.githubusercontent.com/35124840/44327056-deb33380-a45d-11e8-9f11-42d47ffb5803.png)   =    
 ![screenshot from 2018-08-07 19-15-29](https://user-images.githubusercontent.com/35124840/44330232-c4318800-a466-11e8-9209-2876e90b06ff.png)
 
 ![free](https://user-images.githubusercontent.com/35124840/44945848-60f20f00-adf1-11e8-8660-29c015651bdb.png) +  ![big_mario](https://user-images.githubusercontent.com/35124840/44327056-deb33380-a45d-11e8-9f11-42d47ffb5803.png)   =  
  ![free](https://user-images.githubusercontent.com/35124840/44945848-60f20f00-adf1-11e8-8660-29c015651bdb.png) 
  
  
  - **2- If found Mario in frame.**
   
    - Cutting the rejoin of interested which surround Mario.
   
    - The search operation will be on This cutting frame.
   
 ![imageedit_4_5287333350](https://user-images.githubusercontent.com/35124840/44945987-87b14500-adf3-11e8-9cd9-ee1f88b60e7f.png)
 
 
  - ** 2.1- How determine the rejoin of interested? **

    - 1- After found Mario in the all frame  

    - 2- Calculate the top left point and button right point in position Mario in big frame 

    - 3- Subtract constant to the top left point (Mario) and summation constant  button right point (Mario) 
    
![imageedit_41_2046590059](https://user-images.githubusercontent.com/35124840/44946012-0b6b3180-adf4-11e8-8bad-76a649739055.gif)
![imageedit_15_4038166306](https://user-images.githubusercontent.com/35124840/44946020-2342b580-adf4-11e8-96c2-6715205e2b81.gif)

  - **Some of challenge will appear when cutting frame.**

    - 1- If Mario near of the end of frame, part from the rejoin of interested will be out of frame. 
   
![imageedit_8_9845181483](https://user-images.githubusercontent.com/35124840/44946051-acf28300-adf4-11e8-9a87-f046220ef196.gif)
   
  - **Solve:**

    - When Mario is near to end of frame set bounding box by the value of end frame. 

    - Summation the part which out of the frame on the landfill from frame to avoid the size of cutting frame became smaller than size of template. 
   
![imageedit_9_5196929592](https://user-images.githubusercontent.com/35124840/44946052-b380fa80-adf4-11e8-9918-00b9e715ca4a.gif)


   - 2- when search in Cutting frame and find Mario in position X, Y, this position not the correct position in the big frame which will cutting from it the new cutting frame. 

     - **Example:**  
     
 ![imageedit_4_5287333350](https://user-images.githubusercontent.com/35124840/44945987-87b14500-adf3-11e8-9cd9-ee1f88b60e7f.png)    +     ![big_mario](https://user-images.githubusercontent.com/35124840/44327056-deb33380-a45d-11e8-9f11-42d47ffb5803.png)    =            ![imageedit_10_3909610796](https://user-images.githubusercontent.com/35124840/44946094-90a31600-adf5-11e8-9b20-e3df0b2d1677.png)
 
   - Search founded top left point (Mario) in position (X=100, Y=100) 

     This position in big frame: 
     
 ![imageedit_14_9203409824](https://user-images.githubusercontent.com/35124840/44946131-71f14f00-adf6-11e8-9edd-7db710d37d47.gif)
     
  This not the rejoin demanded this position not the correct position of Mario which draw the rectangle surround it. 


   - **Solve:**

     - 1-  When cutting the frame should save the top left point (rejoin) in the big frame. 

     - Example: (X= 400, Y=770) 
     
   ![imageedit_16_2322477947](https://user-images.githubusercontent.com/35124840/44946137-93523b00-adf6-11e8-9331-175546804e22.gif)
 
 - 2-  After Searching in cutting frame founded top left point (Mario) in position (X=100, Y=100) 
 
   - This position should mapped to the correct location in big frame . 

         The correct position = top left point (rejoin) + top left point (Mario)in cutting frame  + constant 
         
  ![imageedit_23_8895122073](https://user-images.githubusercontent.com/35124840/44946138-95b49500-adf6-11e8-92cd-12d51d9adaa5.gif)
  
**In final:** 

  - By using Cutting only the interested rejoin from frame which contain on Mario: 

  - The time reduced from (2 hours 11 minutes) to **(46 minutes)**. 

**But the time still large and not efficient So using Threading Model**


**The second method:**

  - **(2)** Convert code from sequential to parallel by using multi-threading. 

    - By using machine have this information: 
    
|  **information** | **Computer** |
| --- | --- |
| Processor |Up to 8th Gen Intel® Core™ i7 Processor  |
| Graphics |- Intel Integrated Graphics -NVIDIA® GeForce® 940MX(4GB)|
| Memory Ram | 16 GB |
| Thread(s) per core   | 2 |
| Core(s) per socket | 4 |
| Socket(s) | 1|
| CPU(s) = Thread(s) per core  X  Core(s) per socket  X  Socket(s)  | 8 |

 - Can do the convert program to parallel and using threading model by Number_Of_Thread = 8 

   1-partition the video to 8 part. 

   2- distribute each part to thread. 

   3- do search operation parallel in 8 part. 

   4- Aggregation the output of each thread in sequence to create the video. 
   
 **In final:** 

   - By convert code from sequential to parallel by using multi-threading. 

   - The time reduced from (46 minutes) to **(30 minutes)**. 
   
   
 **Summary:** 


|  **Methode** | **Time** |
| --- | --- |
| Search in all frame  | 2 hours 11 minutes  |
| Search in rejoin surround Mario |46 minutes |
| Search in rejoin surround Mario + using Threading model  | 30 minutes |


**Note:** This time is not a good thing. 

  - I think that this function will optimize the time : 

    - 1- convert the image from RGB scale to Gray-scale. 

    - 2- cutting the video to 8 video and read them parallel.
