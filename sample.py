import time
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector

# Initialize the two webcams
cap0 = cv2.VideoCapture(0)
cap1 = cv2.VideoCapture(1)

# Set resolutions for both webcams
for cap in [cap0, cap1]:
    cap.set(3, 640)
    cap.set(4, 480)

detector = HandDetector(maxHands=2)

timer = 0
startbut = False
startGame = False

scores = [0, 0]

while True:
    bg_img = cv2.imread("Resources/BG.png")

    # Read frames from both webcams
    success0, img0 = cap0.read()
    success1, img1 = cap1.read()

    # Resize and crop frames from both cameras
    imgScale0 = cv2.resize(img0, (0, 0), None, 0.875, 0.875)
    imgScale0 = imgScale0[:, 80:480]

    imgScale1 = cv2.resize(img1, (0, 0), None, 0.875, 0.875)
    imgScale1 = imgScale1[:, 80:480]

    # Detect hands in both frames
    hands0, img0 = detector.findHands(imgScale0)
    hands1, img1 = detector.findHands(imgScale1)

    if startGame:
        if startbut is False:
            timer = time.time() - initialTime
            cv2.putText(bg_img, str(int(timer)), (605, 435), cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 4)

            if timer > 3:
                startbut = True
                timer = 0

                if hands0 and hands1:
                    playerMove0 = None
                    playerMove1 = None

                    # Detect fingers for player 1
                    hand0 = hands0[0]
                    fingers0 = detector.fingersUp(hand0)
                    if fingers0 == [0, 0, 0, 0, 0]:
                        playerMove0 = 1  # Rock
                    elif fingers0 == [1, 1, 1, 1, 1]:
                        playerMove0 = 2  # Paper
                    elif fingers0 == [0, 1, 1, 0, 0]:
                        playerMove0 = 3  # Scissors

                # Detect fingers for player 2
                    hand1 = hands1[0]
                    fingers1 = detector.fingersUp(hand1)
                    if fingers1 == [0, 0, 0, 0, 0]:
                        playerMove1 = 1  # Rock
                    elif fingers1 == [1, 1, 1, 1, 1]:
                        playerMove1 = 2  # Paper
                    elif fingers1 == [0, 1, 1, 0, 0]:
                        playerMove1 = 3  # Scissors

                    # Determine winner and update scores
                    if (playerMove0 == 1 and playerMove1 == 3) or (playerMove0 == 2 and playerMove1 == 1) or (
                            playerMove0 == 3 and playerMove1 == 2):
                        scores[1] += 1

                    if (playerMove0 == 3 and playerMove1 == 1) or (playerMove0 == 1 and playerMove1 == 2) or (
                            playerMove0 == 2 and playerMove1 == 3):
                        scores[0] += 1


    bg_img[234:654, 795:1195] = imgScale0
    bg_img[234:654, 92:492] = imgScale1

    cv2.putText(bg_img, str(scores[0]), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 0, 255), 6)
    cv2.putText(bg_img, str(scores[1]), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 0, 255), 6)

    cv2.imshow("BG", bg_img)
    key = cv2.waitKey(1)

    if key == ord('s'):
        # Start the game and initialize variables
        startGame = True
        initialTime = time.time()
        startbut = False



