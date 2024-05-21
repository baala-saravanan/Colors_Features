import cv2
import time
import pandas as pd
import pyttsx3
import subprocess
import gpio as GPIO
from play_audio import GTTSA

play_audio = GTTSA()

#from play_audio import GTTSA
#machine_voice = GTTSA()

GPIO.setup(448, GPIO.IN)  # Exit Button

class Color_detection:
    def __init__(self):
        # Assuming you have a CSV file with color information
        self.csv = pd.read_csv('/home/rock/Desktop/Hearsight/English/colors/colors.csv', header=None, names=["color", "color_name", "hex", "R", "G", "B"])

        # Initialize the text-to-speech engine
        self.engine = pyttsx3.init()

    def get_color_name(self, R, G, B):
        minimum = 10000
        for i in range(len(self.csv)):
            d = abs(R - int(self.csv.loc[i, "R"])) + abs(G - int(self.csv.loc[i, "G"])) + abs(B - int(self.csv.loc[i, "B"]))
            if d <= minimum:
                minimum = d
                cname = self.csv.loc[i, "color_name"]
        return cname

    def color_det(self):
        cap = cv2.VideoCapture(1)  # Change the camera index as needed
        if not cap.isOpened():
#            play_audio.play_machine_audio("camera_is_not_working_so_switch_off_the_HearSight_device_for_some_time_and_then_start_it_again.mp3")
            play_audio.play_machine_audio("hold_on_connection_in_progress_initiating_shortly.mp3")
            play_audio.play_machine_audio("Thank You.mp3")
            subprocess.run(["reboot"])
            return
        cap.release()
        cv2.destroyAllWindows()        
        
        # Initialize video capture
        cap = cv2.VideoCapture(1)
        while True:
            # Capture a frame from the webcam
            ret, frame = cap.read()
            
            if not ret:
                print("Video capture failed.")
#                play_machine_voice.play_machine_audio("video_capture_failed_so_retake_it_again.mp3")
                play_audio.play_machine_audio("video_capture_failed_so_retake_it_again.mp3")
#                break
                return

            # Get the center coordinates of the frame
            height, width, _ = frame.shape
            center_x, center_y = width // 2, height // 2

            # Get the color at the center of the frame
            b, g, r = frame[center_y, center_x]

            # Creating text string to display (Color name and RGB values)
            text = self.get_color_name(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)

            # Speak the color name
#            self.engine.setProperty('voice', 'english_rp+f3')
#            self.engine.setProperty('rate', 200)
            self.engine.setProperty('voice', 'en-gb')
            self.engine.setProperty('rate', 140)
            self.engine.say(self.get_color_name(r, g, b) + "color")
#            self.engine.say(self.get_color_name(r, g, b))
            self.engine.runAndWait()
#            play_audio.play_machine_audio("color.mp3")
#            time.sleep(1)
            print(self.get_color_name(r, g, b) + "color")

            # Display the resulting frame
            cv2.putText(frame, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

            # For very light colors, display text in black color
            if r + g + b >= 600:
                cv2.putText(frame, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

            # Display the resulting frame
#            cv2.imshow("image", frame)

            # Break the loop when the user hits 'esc' key
            #if cv2.waitKey(20) & 0xFF == 27:
                #break
            
            input_state = GPIO.input(448)  # Check the correct GPIO pin for the exit button
            if input_state == True:
#                machine_voice.play_machine_audio("exit_button_pressed.mp3")
                play_audio.play_machine_audio("feature_exited.mp3")
                break

        # Release the webcam and close all OpenCV windows
        cap.release()
#        cv2.destroyAllWindows()
        
# Example usage:
# color_detection = Color_detection()
# color_detection.color_det()
