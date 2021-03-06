import sys
import cv
from datetime import datetime

data_path = "/Users/soswow/Downloads/OpenCV-2.2.0/data/haarcascades"

def detect(image):
    image_size = cv.GetSize(image)

    # create grayscale version
    grayscale = cv.CreateImage(image_size, 8, 1)
    cv.CvtColor(image, grayscale, cv.CV_BGR2GRAY)

    # create storage
    storage = cv.CreateMemStorage(0)
    #cv.ClearMemStorage(storage)

    # equalize histogram
    cv.EqualizeHist(grayscale, grayscale)

    # detect objects
    cascade = cv.Load(data_path+'/haarcascade_frontalface_alt.xml', storage)
    faces = cv.HaarDetectObjects(grayscale, cascade, storage, 1.2, 2, cv.CV_HAAR_DO_CANNY_PRUNING, (50, 50))

    if faces:
        print 'face detected!'
        for (x,y,w,h), n in faces:
            cv.Rectangle(image, (x, y),
                         (x + w, y + h),
                         cv.RGB(0, 255, 0), 3, 8, 0)

if __name__ == "__main__":
#    print "OpenCV version: %s (%d, %d, %d)" % (cv.CV_VERSION,
#                                               cv.CV_MAJOR_VERSION,
#                                               cv.CV_MINOR_VERSION,
#                                               cv.CV_SUBMINOR_VERSION)
    font = cv.InitFont(cv.CV_FONT_HERSHEY_PLAIN, 1, 1)
    print "Press ESC to exit ..."

    # create windows
    cv.NamedWindow('Camera', cv.WINDOW_AUTOSIZE)

    # create capture device
    device = 0 # assume we want first device
    capture = cv.CreateCameraCapture(0)
    cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH, 320)
    cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT, 240)

    # check if capture device is OK
    if not capture:
        print "Error opening capture device"
        sys.exit(1)

    start = datetime.now()
    frame_n, fps = 0, 0
    while 1:
        # do forever

        # capture the current frame
        frame = cv.QueryFrame(capture)
        if frame is None:
            break

        # mirror
        cv.Flip(frame, None, 1)

        # face detection
        detect(frame)

        frame_n += 1
        diff_t = (datetime.now() - start).seconds
        if diff_t > 0:
            fps = frame_n/diff_t
            cv.PutText(frame,"%d FPS" % fps, (0,15), font, cv.RGB(255,255,255))

        # display webcam image
        cv.ShowImage('Camera', frame)

        # handle events
        k = cv.WaitKey(10)

        if k == 0x1b: # ESC
            print 'ESC pressed. Exiting ...'
            break