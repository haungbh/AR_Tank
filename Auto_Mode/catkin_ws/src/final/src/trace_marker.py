import numpy as np
import time
import cv2
import cv2.aruco as aruco

def get_marker(frame):

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    parameters =  aruco.DetectorParameters_create()
    
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    
    if ids is not None:
        
        aruco.drawDetectedMarkers(frame, corners)
        centers = np.mean(corners, axis=2)
        centers = centers.astype(int)
        
        ids = np.reshape(ids, (-1))
        centers = np.reshape(centers, (-1, 2))
        
        return ids, centers
        
    else:
           return None, None
        
if __name__ == '__main__':
    
    cap = cv2.VideoCapture(1)

    font = cv2.FONT_HERSHEY_SIMPLEX
    
    while True:
        _, frame = cap.read()
        
        ids, centers = get_marker(frame)
        
        if ids is not None:
        
            for marker in zip(ids, centers):
                id, center = marker
                cv2.putText(frame, str(id), tuple(center), font, 1, (0,255,0),2,cv2.LINE_AA)
        else:

            cv2.putText(frame, "No Ids", (0,64), font, 1, (0,255,0),2,cv2.LINE_AA)
        
        cv2.imshow("frame", frame)
        
        key = cv2.waitKey(1)
        
        if key == 27:
            print('esc break')
            cap.release()
            break
            