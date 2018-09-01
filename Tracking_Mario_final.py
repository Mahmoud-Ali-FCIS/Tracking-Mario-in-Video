import threading
import cv2
import timeit


# Read Templates and save it in variable
def read_template_images(path):
    template = cv2.imread(str(path))
    w_mario = template.shape[1]
    h_mario = template.shape[0]
    return template, w_mario, h_mario


fire_mario, w_fire_mario, h_fire_mario = read_template_images('fire_mario.png')
big_mario, w_big_mario, h_big_mario = read_template_images('big_mario.png')
mini_mario_jump, w_mini_mario_jump, h_mini_mario_jump = read_template_images('mini_mario_jump.png')
mini_mario, w_mini_mario, h_mini_mario = read_template_images('mini_mario.png')


def write_in_video(list_of_treads):
    output_video = cv2.VideoWriter('Tracking_mario.avi', cv2.VideoWriter_fourcc(*'DIVX'), 30, (1920, 1080))
    for thread_object in list_of_treads:
        for index in range(len(thread_object.out_frame)):
            output_video.write(thread_object.out_frame[index])
    output_video.release()


# Search on marion in frame and Return
def search_mario_on_frame(frame):
    found = False
    top_left_point = 0
    w_mario = 0
    h_mario = 0

    res_match_mini_mario = cv2.matchTemplate(frame, mini_mario, cv2.TM_CCOEFF_NORMED)
    min_val1, max_val_mini_mario, min_loc1, max_loc_mini_mario = cv2.minMaxLoc(res_match_mini_mario)

    res_match_big_mario = cv2.matchTemplate(frame, big_mario, cv2.TM_CCOEFF_NORMED)
    min_val2, max_val_big_mario, min_loc2, max_loc_big_mario = cv2.minMaxLoc(res_match_big_mario)
    if max_val_big_mario >= 0.5 and max_val_big_mario > max_val_mini_mario:
        found = True
        top_left_point = max_loc_big_mario
        w_mario = w_big_mario
        h_mario = h_big_mario
        return found, top_left_point, w_mario, h_mario

    res_match_fire_mario = cv2.matchTemplate(frame, fire_mario, cv2.TM_CCOEFF_NORMED)
    min_val3, max_val_fire_mario, min_loc3, max_loc_fire_mario = cv2.minMaxLoc(res_match_fire_mario)
    if max_val_fire_mario >= 0.5 and max_val_fire_mario > max_val_mini_mario:
        found = True
        top_left_point = max_loc_fire_mario
        w_mario = w_fire_mario
        h_mario = h_fire_mario
        return found, top_left_point, w_mario, h_mario

    if max_val_mini_mario >= 0.4:
        found = True
        top_left_point = max_loc_mini_mario
        w_mario = w_mini_mario
        h_mario = h_mini_mario
        return found, top_left_point, w_mario, h_mario

    res_match_mini_mario_jump = cv2.matchTemplate(frame, mini_mario_jump, cv2.TM_CCOEFF_NORMED)
    min_val4, max_val_mini_mario_jump, min_loc4, max_loc_mini_mario_jump = cv2.minMaxLoc(res_match_mini_mario_jump)
    if max_val_mini_mario_jump >= 0.4:
        found = True
        top_left_point = max_loc_mini_mario_jump
        w_mario = w_mini_mario_jump
        h_mario = h_mini_mario_jump
        return found, top_left_point, w_mario, h_mario

    return found, top_left_point, w_mario, h_mario


def region_of_interest(frame, top_left_point, prev_top_y, prev_top_x):
    top_left_x = top_left_point[0]
    top_left_y = top_left_point[1]
    start_y = top_left_y + prev_top_y - 100
    end_y = top_left_y + prev_top_y + h_big_mario + 100
    start_x = top_left_x + prev_top_x - 100
    end_x = top_left_x + prev_top_x + w_big_mario + 100
    if end_y > 1080:
        end_y = 1080
    if start_y < 0:
        end_y += start_y * -1
        start_y = 0
    if end_x > 1920:
        end_x = 1920
    if start_x < 0:
        start_x = 0
    cut_frame = frame[start_y:end_y, start_x:end_x]
    return cut_frame


def draw_bounding_box(frame, top_left_point, prev_top_y, prev_top_x, w_mario, h_mario):
    bottom_right = (top_left_point[0] + prev_top_x + w_mario, top_left_point[1] + prev_top_y + h_mario)
    cv2.rectangle(frame, (top_left_point[0] + prev_top_x, top_left_point[1] + prev_top_y), bottom_right, 200, 3)
    return frame


def calculate_prev_top_point(top_left_point, prev_top_x, prev_top_y):
    prev_top_x = top_left_point[0] + prev_top_x - 100
    prev_top_y = top_left_point[1] + prev_top_y - 100
    return prev_top_x, prev_top_y


def tracking_mario(frames):
    # you code goes here :D
    new_frame = None
    flag = False
    out_list_of_frames = []
    prev_top_y = 0
    prev_top_x = 0

    for frame in frames:
        frame_all = frame

        if not flag:
            prev_top_x = 0
            prev_top_y = 0
        if flag:
            frame = new_frame
            found, top_left_point, w_mario, h_mario = search_mario_on_frame(frame)
        else:
            found, top_left_point, w_mario, h_mario = search_mario_on_frame(frame_all)

        if found:
            cutting_frame = region_of_interest(frame_all, top_left_point, prev_top_y, prev_top_x)
            new_frame = cutting_frame
            flag = True
            draw_frame = draw_bounding_box(frame_all, top_left_point, prev_top_y, prev_top_x, w_mario, h_mario)
            prev_top_x, prev_top_y = calculate_prev_top_point(top_left_point, prev_top_x, prev_top_y)
            out_list_of_frames.append(draw_frame)
        else:
            out_list_of_frames.append(frame_all)
            flag = False

    return out_list_of_frames


startW = timeit.default_timer()
# Read video of mario and save it as parts in 8 lists = # of Threads
video = []
cap = cv2.VideoCapture('mario.mkv')
while True:
    success, frame = cap.read()

    if success:
        video.append(frame)
    else:
        break


numOfThread = 8
threads = []


class myThread(threading.Thread):
    def __init__(self, thread_id, name, frames):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.frames = frames
        self.out_frame = None

    def run(self):
        print("Starting " + self.name)
        print("{} {}".format(self.name, len(self.frames)))
        self.out_frame = tracking_mario(self.frames)


list_of_threads = []

print("Start threads.....\n")
batch_size = len(video) // numOfThread

for i in range(numOfThread):
    start = i * batch_size
    end = start + batch_size

    if i == numOfThread - 1:
        end = len(video)
    ## i = 1
    ## bs = 200
    ## start << 200
    ## end << 200+200 = 400, that is from 200 to 399 correct

    list_of_threads.append(myThread(i, 'thread_' + str(i), video[start:end]))

for i in range(numOfThread):
    list_of_threads[i].start()

for ti in list_of_threads:
    ti.join()

print("\n threadcount = " + str(threading.active_count()))
print("End threads .....\n")

# Create video and write frames in it
write_in_video(list_of_threads)

stopW = timeit.default_timer()
takeW = stopW - startW
print(takeW)

print("*** End ***")



