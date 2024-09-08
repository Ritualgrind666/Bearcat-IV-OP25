# Raspberry Pi OP25 Bearcat IV "Police Scanner"
Software and hardware to build a system using the shell of a old Electra Bearcat IV Police scanner to monitor and decode signals using OP25.        
![PXL_20240902_032409690small2](https://github.com/user-attachments/assets/84ced60d-4649-4e24-9106-1f39d18b6ae6)


## Features
- Headless OP25 monitoring, trunking, SDR, nbfm monitoring
- Raspberry Pi
- RTL-SDR
- Encorder Button: Selectable Monitoring Channels
- LEDS: light based on function        
- Speakers: Stereo Monitoring
- i2C Liquid Crystal Display: Display Talkgrounps and System Name        
- Power Button        

## Installation
  Add in your raspberrypi ".sh" files.         
  - this will be the description of both the filename and what will be displayed on the LCD 'allListFiles'
  - this will be all the files you want to select and scroll through.
           
  Adjust fileName_ = "/home/pi/op25/TrunkingstartFile.sh".          
  - Replace "TrunkingstartFile.sh" with your starting file that you want the machine to boot to

  Setup to boot on startup
  
## Hardware
 - RaspberryPi
 - Power Connector: 5.5mmx2.1mm 2 Pins DC Power Jack Female Panel Mounting Connector Socket
 - Wall Wart: ELEGOO AC 100V-240V Converter Adapter DC 9V 1A Power Supply US Plug 5.5mm x 2.1mm 1000mA Power Adapter Wall Charger Adapter Compatible with Arduino UNO MEGA with UL FCC CE Certificate
 - Encoder Button: 360 Degree Rotary Encoder Code Switch Digital Potentiometer with Push Button 5 Pins and Knob Cap for Arduino CYT1100
 - Power Button: Latching Pushbutton Switch with LED
 - Liquid Crystal Display: GeeekPi 2-Pack I2C 1602 LCD Display Module 16X2 Character Serial Blue Backlight LCD Module for Raspberry Pi Arduino STM32 DIY Maker Project Nanopi BPI Tinker board Electrical IoT Internet of Things
 - LCD BEZEL: [3D Printed 1602 LCD Bezel](https://www.thingiverse.com/thing:3459425)
 - Speakers: Amazon Basics Computer Speakers for Desktop or Laptop PC , USB-Powered, Black
 - LEDS: PL9823 F5 5mm RGB LED Round P9823 chipset Inside Full Color LED
 - RTL-SDR: Nooelec RTL-SDR v5 SDR - NESDR Smart HF/VHF/UHF (100kHz-1.75GHz) Software Defined Radio. Premium RTLSDR w/ 0.5PPM TCXO, SMA Input & Aluminum Enclosure. RTL2832U & R820T2 (R860)-Based Radio
 - Cable Matters Ground Loop Isolator 3.5mm Noise Isolator Hum Eliminator for Car Audio and More
 - ZS Elec Mini DC 6-24V 24V 12V to 5V 3A USB Buck Voltage Converter Regulator Power Supply Module USB Charging Step Down Voltage Module
 - CableCreation Short Micro USB Cable, USB to Micro USB 24 AWG Triple Shielded Fast Charger Cable, Compatible with PS5/PS4, Raspberry Pi Zero, Chromecast, Phone, 0.5FT/6 inch Black
 - Low Loss SMA Splitter Combiner Cable 6 inch SMA Female to 2-Way SMA Male Flexiable Coaxial RG316 Cord Jack Plug Pigtail 4G LTE Antenna WI-FI
 - CablesOnline 3.5mm (1/8in) Stereo Male Plug to AV 3-Screw Terminal Block Balum Connector, (PL-CN13-2)
 - 6 inch 4-Pole 3.5mm Male Right Angle to 3.5mm Female Stereo Audio Cable Headset Extension Cable Replacement for Beats Dr. Dre Studio iPhone,M to F Audio Cable

## Useful References
 - [OP25 ](https://github.com/boatbod/op25) Linux-based software program that can decode P25 Phase 2 digital voice
 - [radioreference.com](https://www.radioreference.com/) Database of over 224K identified frequencies and 7.1K trunked radio systems
 - [rtl-sdr.com](https://www.rtl-sdr.com) RTL-SDR RTL2832U and software defined radio news and projects
## GUTZ
Not a lot of explanation on wiring and guts of this thing, other than pinouts shown in the code.  Below are some images of my setup and terrible looking wiring connections. I used a dremel to cut a hole in the top for the LCD display.  3D printed and painted a bezel for the display.  cutup a old computer speaker and wired the power button onto the front of the Bearcat.  Lots of hot glue.  Put a power button and plug mounted to rear of the setup using existing holes.      
### TOP VIEW
* * *
![LCDsmall](https://github.com/user-attachments/assets/f0eb8604-9dd8-4497-a288-96f2d74d4142)
![LCDsmall2](https://github.com/user-attachments/assets/10a6b3eb-f3d0-48dd-a2e6-28d6f8f59a31)
![ledred](https://github.com/user-attachments/assets/1be0e533-6c8c-440f-814b-d9a665850181)        
![ledblue](https://github.com/user-attachments/assets/ca5db6b0-1c7d-43fb-809b-6ea92d9e9ebc)
![topview](https://github.com/user-attachments/assets/cd16134b-9f2d-40d3-9de5-147834e10e64)
![speaker](https://github.com/user-attachments/assets/d3248927-c977-4a8b-88ee-48feba8b351f)
![LCD cutout](https://github.com/user-attachments/assets/ccf6ed7e-08ce-47c5-b472-527e419c8526)
![LECD back](https://github.com/user-attachments/assets/b3ab25e4-a019-4a81-a30c-745bed70d804)
![LCD front](https://github.com/user-attachments/assets/52a05b5a-4d2c-421a-8974-f6703b96f5a8)
![smallpanel](https://github.com/user-attachments/assets/028e6e37-24d8-4cfa-8dfd-b1e4d5b0f0aa)
![LCD Back](https://github.com/user-attachments/assets/b0585cbe-9c42-4024-891e-65b292f410a3)
### BOTTOM VIEW
* * *
![bottom](https://github.com/user-attachments/assets/bf5dc53d-8bb9-48f2-bfee-22e989c23925)
![speaker back](https://github.com/user-attachments/assets/0e6b86f3-069a-45e6-b33a-550ec56bb2df)        
### REAR VIEW
* * *
![PXL_20240902_032131690small](https://github.com/user-attachments/assets/f697f63c-b8fb-45ba-b76c-eb93b2bd7dd0)
