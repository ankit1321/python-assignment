from pygame.locals import KEYDOWN, K_ESCAPE, K_q
import pygame
import cv2
import sys
import face_recognition
from transitions import Machine
import time
import argparse
import os
from imutils import paths
import numpy as np


class Bipolar:
    
    def __init__(self,machine_name):
        self.states = ['MachineActive', 'MachineInactive']
        self.machine = Machine(model=self, states=self.states, initial='MachineInactive')
        self.machine.add_transition(trigger='identified', source = 'MachineInactive', dest = 'MachineActive')
        self.machine.add_transition(trigger='not_identified', source = 'MachineActive', dest = 'MachineInactive')
        self.known_face_encoding = []
        self.known_face_names= []
        self.camera = cv2.VideoCapture(0)
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption(machine_name)
        self.screen = pygame.display.set_mode([640, 480])
        self.font_state = pygame.font.SysFont("TIMES NEW ROMAN", 40)
        self.font = pygame.font.SysFont("Arial", 25)
        self.white = (255,255,255)
        self.black = (0,0,0)
        self.green = (0,255,0)
        self.red = (255,0,0)
    
    def read_known_images(self,imagePaths):
        print("[Reading the dataset....]")
        machine_state_status = self.font_state.render('Reading the dataset...',True,self.white,self.black)
        self.screen.blit(machine_state_status,(140,10))
        pygame.display.update()
        for i in imagePaths:
            j = i.split(os.path.sep)[-1]
            k,_ = j.split(".")
            current_image = face_recognition.load_image_file(i)
            current_face_encode = face_recognition.face_encodings(current_image)[0]
            self.known_face_encoding.append(current_face_encode)
            self.known_face_names.append(k)
        print("Done")

    def video_streaming(self):
        if len(self.known_face_encoding)>0:
            self.start_stream()
        else:
            print("No images are trained")

    def start_stream(self):
        while True:

            _, frame = self.camera.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame1 = frame.swapaxes(0, 1)
            pygame.surfarray.blit_array(self.screen, frame1)
            pygame.display.update()
            face_locations = face_recognition.face_locations(frame)
            if len(face_locations)>0:
                if self.state == 'MachineInactive':
                    self.identified()
                unknown_face_encodings = face_recognition.face_encodings(frame,face_locations)
                machine_state_status = self.font_state.render('Machine in Active State',True,self.white,self.black)
                self.screen.blit(machine_state_status,(130,10))    	
                face_names = []
                for face_encoding in unknown_face_encodings:
                    matches = face_recognition.compare_faces(self.known_face_encoding,face_encoding)            
                    
                    name = "unknown"
                    face_distances = face_recognition.face_distance(self.known_face_encoding,face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = self.known_face_names[best_match_index]
                    face_names.append(name)
                    
                    for (top,right,bottom,left),name in zip(face_locations,face_names):
                        if name=="unknown":
                            pygame.draw.rect(self.screen, (255,0,0), pygame.Rect(left, top, right-left, bottom-top),  2) 
                            render_name = self.font.render(name, True,self.red,self.black)
                            self.screen.blit(render_name,(left,top-50))
                            print("unknown")
                            pygame.display.update()
                        else:
                        # for (top,right,bottom,left) in face_locations:
                            pygame.draw.rect(self.screen, (0,255,0), pygame.Rect(left, top, right-left, bottom-top),  2) 
                            render_name = self.font.render(name.upper(), True, self.green,self.black)
                            self.screen.blit(render_name,(left,top-50))
                            print(name)
                            pygame.display.update()

            else:
                if self.state =='MachineActive':
                    self.not_identified()
                    machine_state_status = self.font_state.render('Machine in Inactive State',True,self.white,self.black)
                    self.screen.blit(machine_state_status,(130,10))
                    print("Application is inactive")
            pygame.display.update()
            time.sleep(1)




            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE or event.key == K_q:
                        sys.exit(0)

        pygame.quit()
        cv2.destroyAllWindows()
        


if __name__=="__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--dataset", type=str,
                    default="known_images",
                    help="path to known_images is not given")
    args = vars(ap.parse_args())
    imagePaths = list(paths.list_images(args["dataset"]))
    bipolar = Bipolar("Face Recognition in Pygame")
    bipolar.read_known_images(imagePaths)
    bipolar.video_streaming()
    
    