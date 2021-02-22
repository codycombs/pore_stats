import numpy as np
import oi_file

def grab_frame_video(date,cell,run,tf,channel = '25_50_25x150',camera= 0, image_width = 880, image_height = 140):

	oi_vid = oi_file.video('date')