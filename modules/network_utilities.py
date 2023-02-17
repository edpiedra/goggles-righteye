import socket, cv2, pickle, struct

class NetworkUtilities():

    def _create_client(self, host, port):
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        trying = True 

        while trying:
            try: 
                c.connect((host, port))
                trying = False
            except:
                continue 

        print("[INFO] connected to...{} on {}".format(host, port)) 
        
        return c 

    def _send_color_frame(self, vs, frame):
        _, frame = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
        data = pickle.dumps(frame, 0)
        size = len(data)
        vs.sendall(struct.pack(">L", size) + data)

    def _send_list(self, vs, lst):
        data = pickle.dumps(lst)
        vs.sendall(data)
        
    def _receive_list(self, conn):
        data = conn.recv(1024)
        lst = pickle.loads(data)
        
        return lst
    
    def _destroy(self, s):
        s.shutdown(1)
        s.close()