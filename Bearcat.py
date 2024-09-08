import requests
import json

import sys# from scanner app
import os# from scanner app
import signal# from scanner app

import subprocess
import threading

from datetime import datetime

import time
from time import sleep  # Import sleep function from time modul
import re

import sys
import RPi.GPIO as GPIO

import threading
# Global flag to control the scrolling lights animation
scrolling_active = False
scrolling_lock = threading.Lock()
scrolling_thread = None

## encoder SETUP code - SELECT CHANNELS
#counter = 10
Enc_A = 6  #GPIO LOCATION
Enc_B = 5  #GPIO LOCATION
Enc_BTN = 23 #GPIO LOCATION

# Initialize variables for debouncing
last_state_A = GPIO.HIGH
last_state_B = GPIO.HIGH
counter = 0

# Add a state variable to control callback execution
last_rotation_time = 0
increment = 0
last_increment_time = 0  # Store the time of the last increment
pause_duration = 0.5  # Pause duration in seconds

# NEOPIXEL
#import time ##already above above
import board
import neopixel
from adafruit_led_animation.animation.solid import Solid
from adafruit_led_animation.animation.colorcycle import ColorCycle
from adafruit_led_animation.animation.blink import Blink
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.sequence import AnimationSequence
from adafruit_led_animation.sequence import AnimateOnce
from adafruit_led_animation.color import (
    PURPLE, WHITE, AMBER, JADE, TEAL, PINK, MAGENTA, ORANGE, OLD_LACE, RED, BLUE )

# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D10
# The number of NeoPixels
num_pixels = 8
# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.RGB
pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.025, auto_write=False, pixel_order=ORDER
)

solid = Solid(pixels, color=PINK)
blink = Blink(pixels, speed=0.5, color=JADE)
colorcycle = ColorCycle(pixels, speed=0.2, colors=[RED, BLUE])
chase = Chase(pixels, speed=0.2, color=RED, size=1, spacing=8,reverse=True)
cometblue = Comet(pixels, speed=0.03, color=BLUE, tail_length=24, bounce=False)
comet = Comet(pixels, speed=0.03, color=RED, tail_length=24, bounce=False)
pulse = Pulse(pixels, speed=0.1, color=AMBER, period=3)

COLOR = (100, 50, 150)  # color to blink
CLEAR = (0, 0, 0)  # clear
DELAY = 0.25  # blink rate in seconds
   
###LCD DRIVER SETUP
import smbus
import I2C_LCD_driver
mylcd = I2C_LCD_driver.lcd()

GPIO.setmode(GPIO.BCM)
# Store last state to debounce

##set uri address 
op25uri = 'http://0.0.0.0:8080' ##This is not secure make this your local web address based on json configuration files.
fileName_ = "/home/pi/op25/TrunkingstartFile.sh"  ##starting file on load
allListFiles = [
    "TrunkingstartFile",
    "NOAA",
    "PA-STARNet"
    ]  ### names of trunkfiles
num_Listfile = (len(allListFiles)-1) ##count total trunkfiles subtract one since count starts at zero


def scrolling_lights():
    global scrolling_active

    num_pixels = len(pixels)
    delay = 0.2  # Delay between updates
    current_position = 0

    # Initially, all LEDs are turned on
    pixels.fill((0, 255, 0))  # Set all LEDs to green
    pixels.show()

    while scrolling_active:
        # Check the flag at each iteration
        if not scrolling_active:
            break
        pixels[current_position] = (0, 0, 0)  # Turn off the LED at the current position
        pixels.show()  # Update the display
        current_position = (current_position + 1) % num_pixels  # Move to the next position
        
        # Keep the rest of the LEDs on
        for i in range(num_pixels):
            if i != current_position:
                pixels[i] = (0, 255, 0)
        
        time.sleep(delay)  # Small delay to reduce CPU usage

    # Ensure all LEDs are turned on after scrolling ends
    pixels.fill((0, 255, 0))
    pixels.show()

def start_scrolling():
    """Start the scrolling lights in a separate thread."""
    global scrolling_active
    global scrolling_thread
    with scrolling_lock:
        if not scrolling_active:  # Start a new thread only if animation is not already active
            scrolling_active = True
            scrolling_thread = threading.Thread(target=scrolling_lights)
            scrolling_thread.daemon = True  # Allow the thread to be killed when the main program exits
            scrolling_thread.start()
            #print("Scrolling animation started.")

def stop_scrolling():
    """Stop the scrolling lights animation."""
    global scrolling_active
    with scrolling_lock:
        if scrolling_active:
            scrolling_active = False
            # Wait for the scrolling thread to finish
            if scrolling_thread:
                scrolling_thread.join()  # Ensure the thread has finished before proceeding
            pixels.fill((0, 0, 255))  # Set LEDs to blue
            pixels.show()

def setup_encoder():
    #GPIO.setmode(GPIO.BCM)
    GPIO.setup(Enc_A, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(Enc_B, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(Enc_BTN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(Enc_A, GPIO.BOTH, callback=rotation_decode, bouncetime=28)
       
def police_cycle(wait, flash_count=12):
    for _ in range(flash_count):
        # Flash pattern
        pixels.fill((255, 255, 255))  # White flash
        pixels.show()
        time.sleep(wait / 4)
        pixels.fill((0, 0, 255))  # Blue
        pixels.show()
        time.sleep(wait / 4)
        pixels.fill((255, 0, 0))  # Red
        pixels.show()
        time.sleep(wait / 4)
        
        # Off state for a brief moment
        pixels.fill((0, 0, 0))  # Off
        pixels.show()
        time.sleep(wait / 4)

    # Ensure lights are off after the cycle
    pixels.fill((0, 0, 0))  # Off
    pixels.show()


def start_cycle(n):
    t_end = time.time() + n  ###n= total seconds to run
    while time.time() < t_end:
        bearcatboot.animate()
    


def increment_function(direction):
    global counter, last_increment_time, pause_duration, increment, listFile
    now = time.time()  # Use time.time() to get the current time

    # Only perform increment if the pause duration has passed
    if now - last_increment_time >= pause_duration:
        if direction == "Clockwise":
            counter += 1
            increment = (increment + 1) % num_Listfile
            #print(f"Direction: Clockwise, Counter: {counter}")
        elif direction == "Counter-Clockwise":
            counter -= 1
            increment = (increment - 1 + num_Listfile) % num_Listfile
            #print(f"Direction: Counter-Clockwise, Counter: {counter}")
            
        listFile = allListFiles[increment]
        print(f"Direction: {direction}, Counter: {counter}, Selected File: {listFile}")
        
        last_increment_time = now  # Update the last increment time
        # Update LCD display with new selection
        LCD_CONTROLSELECT()

def rotation_decode(channel):
    global last_state_A, last_state_B, counter

    # Only process if encoder is active
    if not encoder_active:
        return

    state_A = GPIO.input(Enc_A)
    state_B = GPIO.input(Enc_B)
    
    if channel == Enc_A:
        if state_A != last_state_A:
            if state_A != state_B:
                increment_function("Counter-Clockwise")
            else:
                increment_function("Clockwise")
    
    last_state_A = state_A
    last_state_B = state_B
 
def button_pressed(channel):
    """Callback function for button press."""
    global scrolling_active
    print("Encoder button pressed")
    scrolling_active = False  # Stop scrolling
    time.sleep(0.2)
    control_select()

# Add a global variable to control encoder activity
encoder_active = False

def control_select():
    """Handle encoder button press."""
    global self_scanning
    global self_statusLabelText
    global listFile
    global encoder_active
    global scrolling_active  # Ensure this is the global flag used

    if self_scanning:
        self_statusLabelText = "Status: idle"
        stop_scrolling()   # Stop scrolling lights when scanning is done
        os.killpg(os.getpgid(scan.pid), signal.SIGTERM)
        time.sleep(0.2)
        pixels.fill((255, 0, 0))  # Red
        pixels.show()
        time.sleep(0.2)
        self_scanning = False
        encoder_active = True  # Enable encoder when scanning
        LCD_STATUS()

        # Re-add event detection for encoder
        GPIO.remove_event_detect(Enc_A)
        GPIO.add_event_detect(Enc_A, GPIO.BOTH, callback=rotation_decode, bouncetime=28)
    else:
        pixels.fill((0, 255, 0))  # Green
        pixels.show()
        self_scanning = True
        encoder_active = False  # Disable encoder during scanning
        GPIO.remove_event_detect(Enc_A)  # Ensure no conflicting detection
        runOp25(listFile)
        self_statusLabelText = "Status: running"
        LCD_STATUS()
        

        
def setup_gpio_callbacks():
    GPIO.remove_event_detect(Enc_A)
    GPIO.remove_event_detect(Enc_BTN)
    GPIO.add_event_detect(Enc_A, GPIO.BOTH, callback=rotation_decode, bouncetime=28)
    GPIO.add_event_detect(Enc_BTN, GPIO.FALLING, callback=waitfor_edgefunct, bouncetime=50)


def LCD_BOOT():  ## startup display routine
    str_pad = " " * 16
    mylcd.lcd_display_string("<  Bearcat IV  >",1) #add blinkin cursor
    mylcd.lcd_display_string("POLICE.FIRE.EMS ",2)
    police_cycle(0.3)
    pixels.fill((0, 255, 0)) #GREEN
    pixels.show()

LCD_BOOT()    

listFile= allListFiles[0]#option to show first on the dropdown list menu by default.
self_state = True
self_scanning = True
self_statusLabelText="Status: updating"

def jsoncmd(command, arg1, arg2):
    if op25uri == '':
        #print('no uri found')
        return
    if op25uri == 'http://ip_address_to_OP25:port':
        #print('default uri found')
        return
    try:
        response = requests.post(op25uri, json=[{"command": command, "arg1": int(arg1), "arg2": int(arg2)}])
        #print('Response:', response.content)  # Debugging statement
        return response
    except Exception as e:
        #print('Error in jsoncmd:', e)
        return None

       
scan=subprocess.Popen(fileName_, shell=True, stdout=subprocess.PIPE,
                            preexec_fn=os.setsid)  ###Defines subprocess so I can kill it later

                            
####Scanner Integration
def runOp25(trunkFile):
    global scan
    time.sleep(1)
    fileName_ = "/home/pi/op25/"+trunkFile+".sh"
    scan = subprocess.Popen(fileName_, shell=True, stdout=subprocess.PIPE,
                            preexec_fn=os.setsid)
    time.sleep(1)
    tag_str='Connecting...'   
##Update function, runs in a thread to keep checking for new data from the OP25 web server.

def update():
    # Define global variables
    global systemstr
    global tag
    global tag_str
    global grpaddr
    global last_displayed_systemstr
    global scrolling_active  # Ensure this global variable is defined elsewhere
    tag = 'start tag '
    tag_str = 'Connected...'
    systemstr = listFile
    count = 1
    current = ""
    currentAlert = ''
    
    while True:
        try:
            r = jsoncmd("update", 0, 0)
            data = json.loads(r.content)
            LCD_PRINT()  # Update display
            
            for entry in data:
                if isinstance(entry, dict):
                    # Check if entry has 'channels' field
                    if 'channels' in entry:
                        channels = entry['channels']
                        for channel in channels:
                            if channel in entry:
                                channel_data = entry[channel]
                                if isinstance(channel_data, dict):
                                    systemstr = channel_data.get('system', systemstr)
                                    tag = channel_data.get('tag', tag)
                                    tag_str = 'Scanning...' if tag == "Control Channel" else tag.strip() if tag else 'Scanning...'
                                    # Handle scrolling lights
                                    if 'name' in channel_data or 'frequency' in channel_data:
                                        active_channel = True
                                    else:
                                        active_channel = False
                                    if active_channel:
                                        if not scrolling_active:
                                            start_scrolling()
                                    else:
                                        if scrolling_active:
                                            stop_scrolling()
                    
                    # Check if entry has 'top_line' field for trunk data
                    if 'top_line' in entry:
                        systemstr = entry.get('system', systemstr)
                        tag_str = entry['top_line']
                    
                    # Check if 'grpaddr' is in entry
                    if 'grpaddr' in entry:
                        grpaddr = str(entry.get('grpaddr', '0'))
                        enc = str(entry.get('encrypted', '0'))
                        srcaddr = str(entry.get('srcaddr', '0'))
                        
                        if grpaddr == '0':
                            tag_str = 'Scanning...'
                            if not scrolling_active:
                                start_scrolling()
                        elif grpaddr != '0':
                            stop_scrolling()
                            if current != tag:
                                regexp = re.compile('[a-z]|[A-Z]')
                                if regexp.search(tag):
                                    current = tag
                                    count += 1

                    if 'error' in entry:
                        error = str(entry['error'])
                
                if 'json_type' in entry:
                    if entry['json_type'] == 'rx_update':
                        pass  # No actionable data for RX updates
            
            # Check if we need to update scrolling based on tag_str
            if tag_str in ['Scanning...', 'Control Channel']:
                if not scrolling_active:
                    start_scrolling()
            else:
                if scrolling_active:
                    stop_scrolling()

            # Update the display if necessary
            LCD_PRINT()
        
        except Exception as e:
            time.sleep(2)
            if jsoncmd('update', 0, 0) is None:
                pass
            else:
                print('OP25 Instance Connected!')
                LCD_PRINT()
            update()
 
def LCD_PRINT():        
    str_pad = " " * 16
    time.sleep (0.05)
    mylcd.lcd_display_string((tag_str)+str_pad,1)
    mylcd.lcd_display_string((systemstr)+str_pad,2)
    #scroll_text(systemstr + str_pad, 2)
    time.sleep (0.1)

def LCD_STATUS(): ## this show idle or running
    time.sleep (0.1)
    str_pad = " " * 16
    mylcd.lcd_display_string((self_statusLabelText)+str_pad,1)
    if self_scanning == False:
        mylcd.lcd_display_string("SELECT CONTROL=>",2) ### update this to toggle when reloaded
    else:    
        mylcd.lcd_display_string((listFile)+str_pad,2)
        #scroll_text((listFile) + str_pad, 2)
        #print (listFile)
    time.sleep (0.1)

def LCD_CONTROLSELECT(): ##replaced with LCD status
    time.sleep (0.1)
    str_pad = " " * 16
    mylcd.lcd_display_string((listFile)+str_pad,2)
    time.sleep (0.1)
     
print('MODULE LOADED: op25mch_client.py')

if not os.path.exists('logs/'):
    os.mkdir('logs/')

def waitfor_edgefunct(Enc_BTN):
    # if we're here, an edge was recognized
    sleep(0.005) # debounce for 5mSec
    # only show valid edges
    if GPIO.input(Enc_BTN) == 0:
        control_select()

setup_encoder()
setup_gpio_callbacks()

class BearcatIV:
    update()
     
def main():
    
    while True :
        BearcatIV()

if __name__ == '__main__':
        main()
