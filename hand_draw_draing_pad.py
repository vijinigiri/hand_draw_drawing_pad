import cv2
import numpy as np
import os
from cvzone.HandTrackingModule import HandDetector
import time

# ---------------------------------------

def is_line(lst):
    try:
        m=0
        x1,y1,x2,y2 = lst[0][0],lst[0][1],lst[-1][0],lst[-1][1]
        if (x2-x1)!=0:
            m = (y2-y1)/(x2-x1)
        num = np.sqrt(int(m**2+1))
        d = np.abs((lst[:,0]*m-m*x1+y1-lst[:,1])/num)
        if len(d[d>10])>5:
            return False
    except Exception as e:
        pass
    return True
    
def is_circle(lst):
    if np.sqrt(np.sum(np.square(lst[0]-lst[-1])))<10:
        D = np.sqrt(np.sum(np.square(lst-lst[0]),axis=1))
        r=np.max(D)/2
        max_d = lst[np.argmax(D)]
        mid_point = (lst[0][0]+max_d[0])/2,(lst[0][1]+max_d[1])/2
        d = np.sqrt(np.sum(np.square(lst-mid_point),axis=1))
        d = np.abs(d-r)
        if len(d[d<(r/4)])/len(d)>0.6:
            return True,lst[np.argmax(D)]
    return False,None

# ---------------------------------------------

def draw(shape,x1,x2,y1,y2,color,thickness):
    if shape == "line":
        cv2.line(img,(x1,y1),(x2,y2),color,thickness)
    elif shape=="circle":
        cv2.circle(img,((x2+x1)//2,(y2+y1)//2),int((np.sqrt((x2-x1)**2+(y2-y1)**2))/2),color,thickness)
    elif shape == "rectangle":
        cv2.rectangle(img, (x1,y1), (x2,y2),color, thickness)

# -------------------------------------------------


def select_option(x1,y1):
    global colors,n,shapes_active,text,division,dct,grid_lines,grid_check
    m=0
    if y1<100:
        if y1<50:
            try:
                for i in range(1,len(colors)+1):
                    if x1> (40*i)-15 and x1< (40*i)+15:
                        dct['color'] = colors[i][1]
                        colors[i][2]=12
                        m,n=1,i
                    else:
                        colors[i][2]=10
                if m==0:
                    colors[n][2]=12
            except Exception as e:
                print(e)
        else:
            if x1<15*division:
                shapes_active= np.full(6,2)
                text = False
                if x1<division+10:
                    print("line")
                    dct["parameters"] = "line"
                    shapes_active[0]=4
                elif x1>2*division and x1<3*division:
                    print("rectangle")
                    dct["parameters"] = "rectangle"
                    shapes_active[1]=4
                elif x1>3*division and x1<4*division+10:
                    print("circle")
                    dct["parameters"] = "circle"
                    shapes_active[2]=4
                elif x1>4*division and x1<6*division:
                    text = True
                    print("exit text input")
                    shapes_active[3]=4
                elif x1>6*division and x1<8*division:
                    print("erase")
                    dct["parameters"] = "erase"
                    shapes_active[4]=4
                elif x1>8*division and x1<10*division:
                    print("marker")
                    dct["parameters"] = "marker"
                    shapes_active[5]=4
                elif x1>10*division and x1<11*division:
                    if grid_lines!=0:
                        for i in range(100,height,grid_lines):
                            cv2.line(img_grid,(0,i),(width,i),background_color,1)
                    if grid_lines==0:
                        grid_lines = 35
                    elif grid_lines == 35:
                        grid_lines = 49
                    else:
                        grid_lines = 0
                    grid_check=1
        check_thickness()
            
# --------------------------------------------


def nav_bar(nav):
    if nav:
        global division,grid_lines
        division = 40
        nav_img[:]=(0,0,0)
        # colors
        for i,j in colors.items():
            cv2.circle(nav_img,((i)*division,25),j[2],j[1],-1)    
        # shapes
        cv2.line(nav_img,(30,15+50),(division+5,35+50),dct['color'],shapes_active[0])
        cv2.rectangle(nav_img, (2*division,15+50), (3*division,35+50),dct['color'], shapes_active[1])
        cv2.circle(nav_img,(4*division,25+50),12,dct['color'],shapes_active[2])
        
        cv2.putText(nav_img, 'text', (5*division,29+50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, dct['color'],1*int(shapes_active[3]/2), cv2.LINE_AA)
        cv2.putText(nav_img, 'erase', (6*division+5,29+50), cv2.FONT_HERSHEY_SIMPLEX, 0.5 , dct['color'],1*int(shapes_active[4]/2), cv2.LINE_AA)
        cv2.putText(nav_img, 'marker', (8*division,29+50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, dct['color'],1*int(shapes_active[5]/2), cv2.LINE_AA)
        cv2.putText(nav_img, 'grid', (10*division,29+50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, dct['color'],1, cv2.LINE_AA)
        
        cv2.putText(nav_img, f'thickness :{dct['thickness']}', (11*division,29+50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, dct['color'],1, cv2.LINE_AA)
        cv2.line(nav_img,(14*division,75),(division*19,75),dct['color'],shapes_active[0])
        if dct['color']!=(255,255,255):
            cv2.circle(nav_img,(thickness_ball,75),10,(255,255,255),-1)
        else:
            cv2.circle(nav_img,(thickness_ball,75),10,(0,0,255),-1)
        cv2.line(nav_img,(0,100),(width,100),(255,255,255),2)
    
    return  (0,nav_img)

def thickness_bar(x1,y1):
    global thickness_ball
    if y1>50 and y1<100 and x1>14*division and x1< 19*division:
        thickness_ball = x1
        thickness = int((x1-division*15)/10)
        if thickness>=0:
            dct['thickness'] = thickness
        else:
            dct['thickness'] = -1
        check_thickness()
def check_thickness():
    global dct,text
    if (dct["parameters"] in ['line','erase','marker'] or text) and dct["thickness"] in [-1,0]:
        dct["thickness"] = 1

grid_check=1
def grid(grid_check):
    global img_grid
    if grid_lines!=0 and grid_check:
        for i in range(100,height,grid_lines):
            cv2.line(img_grid,(0,i),(width,i),(100,100,100),1)
    return 0

# ------------------------------------------

def track(event,x,y):
    global x1, y1
    global img,img_show,img_grid,img_nav_bar,background_img,img_pointer
    global height,width,background_color,count,count1
    global a,b,c,d,dct,text,lst,points,tab
    global prev_img,grid_check,nav,pointer_color

    if event==1:
        points.clear()
        lst.clear()
        x1,y1,b = x,y,1
        select_option(x1,y1)
        prev_img = img.copy()
        if pointer_color == (0,0,255):
            pointer_color = (255,255,255)
        else:
            pointer_color = (0,0,255)
    elif event == 4:
        pointer_color = dct['color']
        b=0
    if text:
        img = prev_img.copy()
        cv2.putText(img, ''.join(lst), (x1,y1), cv2.FONT_HERSHEY_SIMPLEX, 1, dct['color'], dct['thickness'], cv2.LINE_AA)
        if event==1:
            cv2.putText(img, ''.join(lst), (x1,y1), cv2.FONT_HERSHEY_SIMPLEX, 1, dct['color'], dct['thickness'], cv2.LINE_AA)
    if count1%10==0:
        count1=0
        c,d=x,y        
    if b or tab:
        if y1<100:
            nav = 1
            thickness_bar(x,y)
        elif dct["parameters"]=="marker":
            cv2.circle(img,(x,y),dct['thickness'],dct['color'],-1)
            points.append((x,y))
            if ((c == x and d==y) or tab) and len(points)>10:
                if count >=5 or tab:
                    count = 0 
                    if is_line(np.array(points)):
                        img = prev_img.copy()
                        draw(shape = "line", x1 = x1,x2 = x,y1 = y1,y2 = y,color = dct['color'],thickness = dct['thickness'])
                    else:
                        is_c = is_circle(np.array(points))
                        if is_c[0]:
                            img = prev_img.copy()
                            draw(shape = "circle", x1 = x1,x2 = is_c[1][0],y1 = y1,y2 = is_c[1][1],color = dct['color'],thickness = dct['thickness'])
                count +=1
            count1=count1+1
        elif dct["parameters"] == "erase":
            cv2.circle(img,(x,y),dct['thickness'],background_color,-1)
        tab = 0
    if y1>100:
        if b == 1 and dct["parameters"]!="marker" and dct["parameters"]!="erase":
            img = prev_img.copy()
            draw(shape = dct["parameters"], x1 = x1,x2 = x,y1 = y1,y2 = y,color = dct['color'],thickness = dct['thickness']) 
    
    if dct['thickness']<1:
        cv2.circle(img_pointer,(x,y),3,pointer_color,-1) 
    else:
        cv2.circle(img_pointer,(x,y),dct['thickness'],pointer_color,-1)   
    nav,img_nav_bar = nav_bar(nav)
    grid_check = grid(grid_check)
    img[:102] = img_nav_bar
    img_show = cv2.add(img , img_grid)
    img_show = cv2.add(img_show,img_pointer)
    img_pointer = background_img.copy()

# ----------------------------------------------

x1,y1 = 0,0
division = 40
grid_lines = 0
a,b,c,d,n = 0,0,0,0,0
count,count1,nav = 0,0,1
thickness_ball = 14*division
img_nav_bar = ""
points = []
grid_check = 1
def mouse_tracking(event,x,y,flags,param):
    track(event,x,y)
    
# -----------------------------------------------

def find_path(file_path,img_count):
    while True:
        if not os.path.exists(file_path+str(img_count)+'.jpg'):
            return img_count
        img_count+=1


# ----------------------------------------------

def create_folder():
    current_path = os.getcwd()
    new_folder_name = "dawing_pad"
    new_floder_path = os.path.join(current_path, new_folder_name)
    if not os.path.exists(new_floder_path):
        os.makedirs(new_floder_path)
    return new_floder_path

# --------------------------------------------

height,width = 500,800
background_color = (0,0,0)
lst = []
text = False
tab,t1 = 0,0
floder_path = ''  # path to save drawings
img_count = 1
colors = {1:["red",(0,0,255),15],2:['green',(0,255,0),10],3:['blue',(255,0,0),10],4:["white",(255,255,255),10],5:["yellow",(0,225,255),10],6:["orange",(0, 165, 255),10]}
dct = {"parameters" : "marker","thickness":3,"color":(0,0,255)}
shapes_active = np.full(6,2)
img = np.full((height,width,3),background_color,dtype=np.uint8)
nav_img = np.full((102,width,3),background_color,dtype=np.uint8)
img_show = img.copy()
img_grid = img.copy()
prev_img = img.copy()
background_img = img.copy()
img_pointer = img.copy()
pointer_color = dct['color']
detector = HandDetector(detectionCon=0.8 , maxHands=2)
video = cv2.VideoCapture(0)
prev_lenght,min_length = 0,50
cv2.namedWindow("drawing_pad")
cv2.setMouseCallback("drawing_pad",mouse_tracking)
vid = cv2.VideoCapture(0)
a=0
while True:
    # t1 = time.time()
    key = cv2.waitKey(1)
    try:
        if ((key >= 65 and key <= 122) or (key>=45 and key<=57)) :
                lst.append(chr(key))
        if key == ord('s') and not text:
            if os.path.exists(floder_path):
                file_path = os.path.join(floder_path, 'drawing')
                if not os.path.exists(file_path+str(img_count)+'.jpg'):
                    cv2.imwrite(file_path+str(img_count)+'.jpg',img[102:,])
                    img_count+=1
                    print('img saved')
                else:
                    img_count = find_path(file_path,img_count)
                    cv2.imwrite(file_path+str(img_count)+'.jpg',img[102:])
                    print('img saved')
            else:
                print('given path is invalid')
                floder_path = create_folder()
                print(f'file will be stored in {floder_path}')
                file_path = os.path.join(floder_path, 'drawing')
                img_count = find_path(file_path,img_count)
                cv2.imwrite(file_path+str(img_count)+'.jpg',img[102:])
                print('img saved')
            lst.clear()
        elif key == 13 and not text: # enter
            if lst[0] == 't' and len(lst)>1:
                    dct['thickness'] = int(''.join(lst[1:])) 
            lst.clear()
        elif key == 9:
            tab = 1
        elif key == 8: # (back space ) clear text 
                lst.pop()
    # -------------------------------------------
        ret,frame = video.read()
        frame = cv2.resize(cv2.flip(frame,1), (width+200, height+200))
        hands,img_hand=detector.findHands(frame)
        if hands:
            x,y = hands[0]['center']
            lmlist = hands[0]
            length, info,img_hand = detector.findDistance(lmlist["lmList"][4][:2], lmlist["lmList"][8][:2],img_hand)
            if (prev_lenght >= min_length and length < min_length):
                event=1
                a=1
            elif (prev_lenght < min_length and length >= min_length):
                event=4
                a=0
            else:
                event=0

            if x<100:
                x=0
            if y<100:
                y=0

            prev_lenght = length
            track(event,x-100,y-100)
            if a==1:
                cv2.putText(img_hand,'activate',(20,460), cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),1,cv2.LINE_AA)
            else:
                cv2.putText(img_hand,'',(20,460), cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),1,cv2.LINE_AA)
            
    # ----------------------------------------------
    except Exception as e:
        print('invalid value')
        lst.clear()
        print(e)
    cv2.imshow("Frame",img_hand[:-200])
    cv2.imshow("drawing_pad",img_show)
    if key == 0:
        break
    # print(time.time()-t1)
cv2.destroyAllWindows()