import UnicornPy
import numpy as np
import csv
import pandas as pd
from datetime import date
from datetime import datetime
import os
import time
import random
from Trial_struct import *
import gui
import get_param
import serial
import pygame
import sys
from os.path import exists
from os import walk

arduinoData = serial.Serial('COM6', 115200)
arduinoData2 = serial.Serial('COM7', 115200)

class Start_Recording():
    def __init__(self, len_trial_rec, eeg_filename, event_filename ,TestsignaleEnabled ,trial_number,  patient_name, Unicorn_id, task_number):
        self.AcquisitionDurationInSeconds =  len_trial_rec
        self.EEG_file_name = eeg_filename
        self.event_file_name = event_filename
        self.numberOfAcquiredChannels = 0
        self.configuration = 0
        self.SamplingRate = 0
        self.FrameLength = 1
        self.device = 0
        self.TestsignaleEnabled = TestsignaleEnabled
        self.patient_name = patient_name
        self.trial = trial_number
        self.unicorn_id = Unicorn_id
        self.task_number = task_number
        self.header = 'FZ, FC1, FC2, C3, CZ, C4, CPZ, PZ, AccelX, AccelY, AccelZ, GyroX, GyroY, GyroZ, Battery, Sample, Unkown'

    def eeg_devices(self):
        if self.unicorn_id == False:
            deviceList = UnicornPy.GetAvailableDevices(True)

            if len(deviceList) <= 0 or deviceList is None:
                raise Exception("No device available.Please pair with a Unicorn first.")

            # Print available device serials.
            print("Available devices:")
            i = 0
            for device in deviceList:
                print("#%i %s" % (i,device))
                i+=1

            # Request device selection.
            print()
            deviceID = int(input("Select device by ID #"))
            if deviceID < 0 or deviceID > len(deviceList):
                raise IndexError('The selected device ID is not valid.')
            else:
                unicorn_dev_id = deviceList[deviceID]
        else:
            unicorn_dev_id = self.unicorn_id

        return unicorn_dev_id

    def eeg_connect(self):
        dev_ID = self.eeg_devices()
        print("Trying to connect to '%s'." %dev_ID)
        self.device = UnicornPy.Unicorn(dev_ID)
        print("Connected to '%s'." %dev_ID)
        print()
        self.numberOfAcquiredChannels = self.device.GetNumberOfAcquiredChannels()
        self.configuration = self.device.GetConfiguration()
        self.SamplingRate = UnicornPy.SamplingRate


    def start_acquisition(self, eeg_path, event_path):
        #running for different trials
        states = self.choose_random_state(self.trial)
        
        while True:
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

            self.device.StartAcquisition(self.TestsignaleEnabled)
            for j in range(self.trial):
                #Trial 

                receiveBufferBufferLength = self.FrameLength * self.numberOfAcquiredChannels * 4
                receiveBuffer = bytearray(receiveBufferBufferLength)
                
                print("Data acquisition started.")

                numberOfGetDataCalls = int(self.AcquisitionDurationInSeconds * self.SamplingRate / self.FrameLength)
                # Limit console update rate to max. 25Hz or slower to prevent acquisition timing issues.                   
                consoleUpdateRate = int((self.SamplingRate / self.FrameLength) / 25.0)
                if consoleUpdateRate == 0:
                    consoleUpdateRate = 1

            
                sr = self.SamplingRate
                self.current_eeg = eeg_path + "/" + str(j) + "_"+ self.task_number + "_"+ self.EEG_file_name
                file = open(self.current_eeg, "a")
                file.write(self.header)
                file.write('\n')

                initial_data = []
                # i is sample point in trial j 
                count = 0
                for i in range (0,numberOfGetDataCalls):
                    # Receives the configured number of samples from the Unicorn device and writes it to the acquisition buffer.
                    self.device.GetData(self.FrameLength,receiveBuffer,receiveBufferBufferLength)
                
                    # Convert receive buffer to numpy float array 
                    dataa = np.frombuffer(receiveBuffer, dtype=np.float32, count=self.numberOfAcquiredChannels * self.FrameLength)
                    data = np.reshape(dataa, (self.FrameLength, self.numberOfAcquiredChannels))
                    #write 
                    data[0][15] = count 

                    gui.display_surface.fill((255, 255, 255))
                    if j == 0:
                        gui.display_surface.blit(gui.text4, gui.textRect4)

                    elif j == 1:
                        gui.display_surface.blit(gui.text5, gui.textRect5)

                    elif j == 2:
                        gui.display_surface.blit(gui.text6, gui.textRect6)

                    elif j == 3:
                        gui.display_surface.blit(gui.text7, gui.textRect7)

                    elif j == 4:
                        gui.display_surface.blit(gui.text8, gui.textRect8)

                    AR = Arduino(initial_data, count , sr, states[j],arduinoData,arduinoData2)
                    if self.task_number =="task_1" or self.task_number =="task_3" or self.task_number =="task_4" or self.task_number =="task_5" :
                        initial_data = AR.task_1()

                    elif self.task_number == "task_2":
                        initial_data = AR.task_2()

                    np.savetxt(file,data,delimiter=',',fmt='%.3f',newline='\n')
                    
                    pygame.display.update()
                    # Update console to indicate that the data acquisition is running.
                    count += 1
                    if count % consoleUpdateRate == 0:
                        print('.',end='',flush=True)

                    

                self.current_event = event_path[0] + "/" + str(j) + "_"+ self.task_number + "_"+ self.event_file_name
                array = np.array(initial_data)
                pd.DataFrame(array).to_csv(  self.current_event ,header=["glass_event", "Buzzer_event","motor_turning_event","events","TursnStart", "sample_number"], index=False)
                file.close()

                #convert a list to data frame to store in a csv file 
                print("Data ", str(j) , "acquisition stopped.")

            print("Disconnected from Unicorn")
            self.TextFile(event_path[1])
            del receiveBuffer
            self.device.StopAcquisition()
            del self.device
            sys.exit()
        
    def TextFile(self,path):

        today = date.today()
        dateee = today.strftime("%Y/%m/%d")

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        save_path = path + "/"
        complete_path = os.path.join(save_path, self.patient_name +".txt")

        task = ["task_1","task_2","task_3","task_4","task_5"]
        count = [0,0,0,0,0]
        total = 0
        trial_num = {"task_1": 0, "task_2": 0,"task_3":0,"task_4":0,"task_5":0 }

        for j,i in enumerate(task):
            dir_path = os.path.join( path, i)
            
            for x in os.walk(dir_path):
                if x[0].find('event') !=-1:
                    count[j] += len(x[2])
                    trial_num[i] = len(x[2])
                    total += len(x[2])
            

        

        file_exists = exists(complete_path)
        if file_exists:
            with open(complete_path, 'a') as f:
                f.write('\n')
                f.write(''.join(task[0] + " : " + str(count[0])  + " csv files" + "  ( trial number =" + str(trial_num["task_1"]) +")"))
                f.write('\n')
                f.write(''.join(task[1] + " : " + str(count[1]) + " csv files"  + "  ( trial number =" + str(trial_num["task_2"]) +")"))
                f.write('\n')
                f.write(''.join(task[2] + " : " + str(count[2]) + " csv files"  + "  ( trial number =" + str(trial_num["task_3"]) +")"))
                f.write('\n')
                f.write(''.join(task[3] + " : " + str(count[3]) + " csv files"  + "  ( trial number =" + str(trial_num["task_4"]) +")"))
                f.write('\n')
                f.write(''.join(task[4] + " : " + str(count[4]) + " csv files"  + "  ( trial number =" + str(trial_num["task_5"]) +")"))
                f.write('\n')
                f.write(''.join("Total " + " : " + str(total) + " csv files"))
                f.write('\n')
                f.write('------------------------------------------------------------------')
                f.write('\n')
                f.write('\n')
            f.close()

        else:
            more_lines = ["Patient_name :" + self.patient_name, "Date :" +dateee , "Time :" +current_time]
            with open(complete_path, 'w') as f:
                f.write('\n'.join(more_lines))
                f.write('\n')
                f.write('\n')
                f.write('\n')
                f.write('\n')
                f.write(''.join(task[0] + " : " + str(count[0]) + " csv files" + "  ( trial number =" + str(trial_num["task_1"]) +")"))
                f.write('\n')
                f.write(''.join(task[1] + " : " + str(count[1]) + " csv files" + "  ( trial number =" + str(trial_num["task_2"]) +")"))
                f.write('\n')
                f.write(''.join(task[2] + " : " + str(count[2]) + " csv files" + "  ( trial number =" + str(trial_num["task_3"]) +")"))
                f.write('\n')
                f.write(''.join(task[3] + " : " + str(count[3])+ " csv files"  + "  ( trial number =" + str(trial_num["task_4"]) +")"))
                f.write('\n')
                f.write(''.join(task[4] + " : " + str(count[4])+ " csv files"  + "  ( trial number =" + str(trial_num["task_5"]) +")"))
                f.write('\n')
                f.write(''.join("Total " + " : " + str(total)+ " csv files"))
                f.write('\n')
                f.write('------------------------------------------------------------------')
                f.write('\n')
                f.write('\n')
            f.close()

    def make_dir(self, pathname):
        os.chdir('C:\\Users\\annacetera\\Documents')
        curworkdir = os.getcwd()
        path = os.path.join(curworkdir, "EEGdata") 
        #patient_name
        today = date.today()
        
        dateee = today.strftime("%Y%m%d")
        path = os.path.join(path, dateee) 

        directory = self.patient_name
        path = os.path.join(path, directory)  

        directory = self.task_number
        path1 = os.path.join(path, directory)

        #add time to directory
        now = datetime.now()
        current_time = now.strftime("%H%M%S")
        path2 = os.path.join(path1, current_time)


        directory = pathname
        path3 = os.path.join(path2, directory)  

        if not os.path.exists(path3):
            os.makedirs(path3)  
        return path3, path

    def choose_random_state(self,trial_number):
        states = [1,2]
        a = states[random.randint(0, len(states)-1)]
        b = states[random.randint(0, len(states)-1)]
        final_state = [0,a,0,b,0]
        trial_list = []
        
        for i in range(0,trial_number):
            a = []
            b = []
            pre_state = 0
            for j,i in enumerate(final_state):
                if i ==1 or i==2:
                    if pre_state ==1:
                        final_state[j] = 2
                        b.append(2)
                        pre_state = 2
                    elif pre_state==2:
                        final_state[j] = 1
                        b.append(1)
                        pre_state = 1
                        
                    else:
                        final_state[j] = states[random.randint(0, len(states)-1)]
                        b.append(final_state[j])
                        pre_state = final_state[j]
                else:
                    a.append(0)
            
            trial_list.append([a[0],b[0],a[1],b[1],a[2]])
        return trial_list



    def main(self):
        eeg_path , secpath = self.make_dir("eeg")
        event_path = self.make_dir("event")
        self.eeg_connect()
        self.start_acquisition(eeg_path, event_path)
        
        

data_recording = Start_Recording(len_trial_rec = get_param.Trial_duration, 
                                eeg_filename = "EEG.csv", 
                                event_filename ="Event.csv" ,
                                TestsignaleEnabled = False, 
                                trial_number= get_param.Trial_number ,
                                patient_name= get_param.Username,
                                Unicorn_id  = get_param.Unicorn_ID,
                                task_number = get_param.task_list)
data_recording.main()








