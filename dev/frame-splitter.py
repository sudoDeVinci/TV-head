import cv2
vidcap = cv2.VideoCapture('dev/images/random/svet.gif')
success,image = vidcap.read()
count = 0
while success:
  cv2.imwrite(f"dev/images/svet/svet-{str(count).zfill(4)}.png", image)     # save frame as JPEG file      
  success,image = vidcap.read()
  # print('Read a new frame: ', success)
  count += 1
