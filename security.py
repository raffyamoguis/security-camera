import cv2
import time
import datetime

#Access video camera
cap = cv2.VideoCapture(0)

#Create a facial and body classifier with opencv
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_fullbody.xml")

detection = False
detection_stopped_time = None
timer_started = False
SECONDS_TO_RECORD_AFTER_DETECTION = 5

framesize = (int(cap.get(3)), int(cap.get(4)))#Set frame size
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
#out = cv2.VideoWriter("video.mp4", fourcc, 20.0, framesize)

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)#Flip the camera on certain laptop webcam

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    bodies = face_cascade.detectMultiScale(gray, 1.3, 5)

    #Security camera video logic
    if len(faces) + len(bodies) > 0:
        if detection:
            timer_started = False
        else:
            detection = True
            current_time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
            out = cv2.VideoWriter(f"{current_time}.mp4", fourcc, 20.0, framesize)
            print("Started recording")
    elif detection:
        if timer_started:
            if time.time() - detection_stopped_time >= SECONDS_TO_RECORD_AFTER_DETECTION:
                detection = False
                timer_started = False
                out.release()
                print("Stop recording")
        else:
            timer_started = True
            detection_stopped_time = time.time()

    if detection:
        out.write(frame)

    #draw rectangle if face is detected
    for (x, y, width, height) in faces:
       cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 255, 0), 3)

    cv2.imshow("Camera", frame)#Show the window camera

    #Exit the camer using the q key
    if cv2.waitKey(1) == ord('q'):
        break

out.release()
cap.release()
cv2.destroyAllWindows()