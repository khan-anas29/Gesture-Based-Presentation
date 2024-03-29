# starting with the web cam
import os
import cv2
from cvzone.HandTrackingModule import HandDetector

# # Variables
# Camera Width & Height
width,height= 1200, 720
# Folder Path
folderpath="img"


# Camera setup
cap= cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

# getting Presentation Images
# We need to sort this to 10 will be at last not after 1
imgPath=sorted(os.listdir(folderpath),key=len)
# print(imgPath)

# Number of Image to show
imgNum= 0

# Small img of webcam
# These are numbers that are actual/8
hsImg,wsImg=(120*1),(213*1)


# Hand Detector
# if 80% surity of hands then detect as hands
detector = HandDetector(detectionCon=0.8,maxHands=1)
gestureThreshold=400
buttonPressed=False
buttonCounter=0
buttonDelay=15 #Frames to check delay it can vary from camera to Camera


while True:
    # Import Images
    sucess,img=cap.read()
    # Flip the image to get hand Movement right Horizontal=1,Vertical=0
    img=cv2.flip(img,1 )

    # Slide part
    fullimg=os.path.join(folderpath,imgPath[imgNum])
    CurrentImg=cv2.imread(fullimg)
    # Resizing because slide too large for display
    CurrentImgResize=cv2.resize(CurrentImg,(width,height))

    # finding hands on img i.e webcam
    hands, img= detector.findHands(img,flipType=False)
    # Threshold line to start detection (img,start,end,color,thickness)
    cv2.line(img,(0,gestureThreshold),(1400,gestureThreshold),(0,255,0),10)





    if hands and buttonPressed is False:
        hand=hands[0]

        fingers=detector.fingersUp(hand)
        # print(fingers)
        # Center Points
        cx, cy =hand['center']

        if cy<=gestureThreshold: #If hand is above or at face level
            # Gesture 1 - Left
            if fingers==[0,0,0,0,0]:
                print("Left")
                if imgNum>0: #Changing Backwards
                    imgNum-=1
                    buttonPressed=True
            # Gesture 2 - Right
            if fingers==[1,0,0,0,1]:
                print("Right")
                if imgNum<(len(imgPath)-1): #Changing Forward
                    imgNum+=1
                    buttonPressed=True

    # button Pressed Iterations (Getting Back to False to Click Again)
    if buttonPressed:
        buttonCounter +=1
        if buttonCounter>buttonDelay:
            buttonCounter=0
            buttonPressed=False




    # Adding Small Webcam Image on Slide
    imgSmall=cv2.resize(img, (wsImg, hsImg))
    # We don't know the width and height of slide thus getting them
    hslide, wslide, _ = CurrentImgResize.shape

    # putting small webcam on right side
    # height 0 to height of web image
    # widht  (actual widht of slide - width of small img) to  width of slide
    CurrentImgResize[0:hsImg, wslide-wsImg:wslide] = imgSmall

    cv2.imshow("WEBCAM", img)
    cv2.imshow("Slides", CurrentImgResize)
    key= cv2.waitKey(1)
    # Adding if to close webcam and break the loop by pressing "Q"
    if key == ord("q"):
        break