import cv2, sys, os, time 
import modules.network_utilities as nu 

os.system("pkill -o -u pi sshd")
time.sleep(0.5) 

net = nu.NetworkUtilities()
pc_c = net._create_client("Eddy-Linux.local", 8088)
program_mode = pc_c.recv(1024).decode("utf-8")

camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

if not camera.isOpened():
    print("[ERROR] unable to open righteye camera...")
    sys.exit()

start_time = time.time()
    
while program_mode!="QUIT":
    ret, frame = camera.read()
    
    if not ret:
        print("[ERROR] unable to read frame...")
        break
    
    lps = (1.0 / (time.time()-start_time))
    start_time = time.time()
    
    text = "lps: {:.2f}".format(lps)
        
    cv2.putText(
        frame, text, (10, 235), cv2.FONT_HERSHEY_SIMPLEX,
        0.5, (255,255,255), 2, cv2.FILLED
    )
    
    net._send_color_frame(pc_c, frame)
    program_mode = pc_c.recv(1024).decode("utf-8")
    
camera.release()
net._destroy(pc_c)