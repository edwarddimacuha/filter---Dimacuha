#import necessary libraries
import face_recognition
import cv2

#camera class for the on and off function
class Camera:
    def turn_on(self,no):
        self.no = no
        cam = cv2.VideoCapture(self.no)
        return cam
    def turn_off(self,cam):
        self.cam = cam
        self.cam = self.cam.release()
        cv2.destroyAllWindows()
        
#graphics class for setting the offset(position) of the graphics and draw function to apply the graphics to face landmarks
class Graphics:
    def height_offset(self, left_eye, offset):
        self.left_eye = left_eye
        self.offset = offset
        height_offset =  self.left_eye + offset
        return height_offset
    def width_offset(self, left_eye, offset):
        self.left_eye = left_eye
        width_offset = self.left_eye + offset
        return width_offset
    def draw(self,height, width, frame_height, frame_width, frame, h_offset, w_offset,img):
        self.height = height
        self.width = width
        self.frame_height = frame_height
        self.frame_width = frame_width
        self.frame = frame
        self.h_offset = h_offset
        self.w_offset = w_offset
        self.img = img
        for i in range(0,self.height):
            if self.h_offset + i >= self.frame_height:
                break
            for j in range(0, self.width):
                if self.img[i,j][3] != 0:
                    if self.w_offset + j >= self.frame_width:
                        break
                    else:
                        self.frame[self.h_offset + i,self.w_offset + j] = self.img[i,j]

cam = Camera()
graphics = Graphics()
cam = cam.turn_on(0)

#read graphics from their directory
glass = cv2.imread("./sprites1/eyeglass.png",-1)
beard = cv2.imread("./sprites1/moustache.png",-1)
crown = cv2.imread("./sprites1/toga.png",-1)
border = cv2.imread("./sprites1/wow.png",-1)
heart_l = cv2.imread("./sprites1/heart1.png",-1)
heart_r = cv2.imread("./sprites1/heart2.png",-1)
smile = cv2.imread("./sprites1/smile.png",-1)

#convert their colors in order to be read by cv2
smile = cv2.cvtColor(smile,cv2.COLOR_BGR2BGRA)
heart_l = cv2.cvtColor(heart_l,cv2.COLOR_BGR2BGRA)
heart_r = cv2.cvtColor(heart_r,cv2.COLOR_BGR2BGRA)
glass = cv2.cvtColor(glass,cv2.COLOR_BGR2BGRA)
beard = cv2.cvtColor(beard,cv2.COLOR_BGR2BGRA)
crown = cv2.cvtColor(crown,cv2.COLOR_BGR2BGRA)
border = cv2.cvtColor(border,cv2.COLOR_BGR2BGRA)

while(cam.isOpened()):
    ret, frame = cam.read()
    fh,fw,fc = frame.shape
    face_locations = face_recognition.face_locations(frame)
    face_landmarks_list = face_recognition.face_landmarks(frame)
    im = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
    #set the coordinates and size of the static border image
    border = cv2.resize(border, (110,110), (80,80))
    x_offset = y_offset = 10
    im[y_offset:y_offset + border.shape[0], x_offset:x_offset + border.shape[1]] = border
    
    #resize each graphics based on the facial landmarks
    for elements in face_landmarks_list:
        glass = cv2.resize(glass, (50+(int(elements['right_eye'][3][0]) - int(elements['left_eye'][0][0])), (50+(int(elements['left_eye'][4][1]) + int(elements['left_eye'][5][1]))//2) - ((int(elements['left_eye'][1][1]) + int(elements['left_eye'][2][1]))//2)))
        beard = cv2.resize(beard, ((int(elements['right_eye'][3][0]) - int(elements['left_eye'][0][0])), (10+(int(elements['left_eye'][4][1]) + int(elements['left_eye'][5][1]))//2) - ((int(elements['left_eye'][1][1]) + int(elements['left_eye'][2][1]))//2)))
        crown = cv2.resize(crown, (100+(int(elements['right_eye'][3][0]) - int(elements['left_eye'][0][0])), (120+(int(elements['left_eye'][4][1]) + int(elements['left_eye'][5][1]))//2) - ((int(elements['left_eye'][1][1]) + int(elements['left_eye'][2][1]))//2)))
        heart_l = cv2.resize(heart_l, (50+(int(elements['right_eye'][3][0]) - int(elements['left_eye'][0][0])), (50+(int(elements['left_eye'][4][1]) + int(elements['left_eye'][5][1]))//2) - ((int(elements['left_eye'][1][1]) + int(elements['left_eye'][2][1]))//2)))
        heart_r = cv2.resize(heart_r, (50+(int(elements['right_eye'][3][0]) - int(elements['left_eye'][0][0])), (50+(int(elements['left_eye'][4][1]) + int(elements['left_eye'][5][1]))//2) - ((int(elements['left_eye'][1][1]) + int(elements['left_eye'][2][1]))//2)))
        smile = cv2.resize(smile, (10+(int(elements['right_eye'][3][0]) - int(elements['left_eye'][0][0])), (40+(int(elements['left_eye'][4][1]) + int(elements['left_eye'][5][1]))//2) - ((int(elements['left_eye'][1][1]) + int(elements['left_eye'][2][1]))//2)))

        #set offset for each graphics for proper positioning
        height_offset = graphics.height_offset(elements['left_eye'][2][1], -10)
        width_offset = graphics.width_offset(elements['left_eye'][0][0], -23)
        height_offset1 = graphics.height_offset(elements['left_eye'][2][1], 50)
        width_offset1 = graphics.width_offset(elements['left_eye'][0][0], 0)
        height_offset2 = graphics.height_offset(elements['left_eye'][2][1], -150)
        width_offset2 = graphics.width_offset(elements['left_eye'][0][0], -50)
        height_offset3 = graphics.height_offset(elements['left_eye'][2][1], 10)
        width_offset3 = graphics.width_offset(elements['left_eye'][0][0], -200)
        height_offset4 = graphics.height_offset(elements['left_eye'][2][1], 10)
        width_offset4 = graphics.width_offset(elements['left_eye'][0][0], 160)
        height_offset5 = graphics.height_offset(elements['left_eye'][2][1], 85)
        width_offset5 = graphics.width_offset(elements['left_eye'][0][0], 0)

        #draw the graphics to the facial coordinates
        gh,gw,gc = glass.shape
        #graphics.draw(gh, gw, fh, fw, im, height_offset, width_offset, glass)
        for i in range(0,gh):
            if height_offset + i >= fh:
                break
            for j in range(0, gw):
                if glass[i,j][3] != 0:
                    if width_offset + j >= fw:
                        break
                    else:
                        im[height_offset + i,width_offset + j] = glass[i,j]

        bh,bw,bc = beard.shape
        #graphics.draw(bh, bw, fh, fw, im, height_offset1, width_offset1, beard)
        for i in range(0,bh):
            if height_offset1 + i >= fh:
                break
            for j in range(0, bw):
                if beard[i,j][3] != 0:
                    if width_offset1 + j >= fw:
                        break
                    else:
                        im[height_offset1 + i,width_offset1 + j] = beard[i,j]

        ch,cw,cc = crown.shape
        #graphics.draw(ch, cw, fh, fw, im, height_offset2, width_offset2, crown)
        for i in range(0,ch):
            if height_offset2 + i >= fh:
                break
            for j in range(0, cw):
                if crown[i,j][3] != 0:
                    if width_offset2 + j >= fw:
                        break
                    else:
                        im[height_offset2 + i,width_offset2 + j] = crown[i,j]

        hh,hw,hc = heart_l.shape
        #graphics.draw(hh, hw, fh, fw, im, height_offset3, width_offset3, heart_l)
        for i in range(0,hh):
            if height_offset3 + i >= fh:
                break
            for j in range(0, hw):
                if heart_l[i,j][3] != 0:
                    if width_offset3 + j >= fw:
                        break
                    else:
                        im[height_offset3 + i,width_offset3 + j] = heart_l[i,j]

        hh,hw,hc = heart_r.shape
        #graphics.draw(hh, hw, fh, fw, im, height_offset4, width_offset4, heart_r)
        for i in range(0,hh):
            if height_offset4 + i >= fh:
                break
            for j in range(0, hw):
                if heart_r[i,j][3] != 0:
                    if width_offset4 + j >= fw:
                        break
                    else:
                        im[height_offset4 + i,width_offset4 + j] = heart_r[i,j]

        sh,sw,sc = smile.shape
        #graphics.draw(sh, sw, fh, fw, im, height_offset5, width_offset5, smile)
        for i in range(0,sh):
            if height_offset5 + i >= fh:
                break
            for j in range(0, sw):
                if smile[i,j][3] != 0:
                    if width_offset5 + j >= fw:
                        break
                    else:
                        im[height_offset5 + i,width_offset5 + j] = smile[i,j]


    cv2.imshow("WOW Filter", im)
    #reread the images to avoid blurring
    glass = cv2.imread("./sprites1/eyeglass.png",-1)
    beard = cv2.imread("./sprites1/moustache.png",-1)
    crown = cv2.imread("./sprites1/toga.png",-1)
    border = cv2.imread("./sprites1/wow.png",-1)
    heart_l = cv2.imread("./sprites1/heart1.png",-1)
    heart_r = cv2.imread("./sprites1/heart2.png",-1)
    smile = cv2.imread("./sprites1/smile.png",-1)

    if cv2.waitKey(1) == 27:
        break

#cam.turn_off(cam)
cam.release()
cv2.destroyAllWindows()

