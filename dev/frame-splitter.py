import cv2
vidcap = cv2.VideoCapture('dev/images/knife/Untitled_Artwork.mp4')
success,image = vidcap.read()
count = 0
while success:
  cv2.imwrite(f"dev/images/knife/Untitled_Artwork-{str(count).zfill(4)}.png", image)     # save frame as JPEG file      
  success,image = vidcap.read()
  # print('Read a new frame: ', success)
  count += 1
