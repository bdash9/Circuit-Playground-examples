# The Perfect Pitch Machine
# By Isaac Wellish
# Creative Commons Licence (Anyone can use and hack the code, just give attributions please!)
#
#
# Big thanks to Adafruit! 
# Much of this code was adapted from Adafruit's Circuit Playground Sound Meter tutorial found here: 
# https://learn.adafruit.com/adafruit-circuit-playground-express/playground-sound-meter
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


#LET'S BEGIN


#import neccesarry libraries
import audiobusio
import board
import array
import math
import time
from digitalio import DigitalInOut, Direction, Pull
import audioio
import neopixel
import digitalio

# Threshhold for loudness of sound needed to trigger current pitch
blowThresshold = 5000

# debounce time, how long the debounce time should be to prevent multiple button triggers in one press
debounceTime = 0.2

# pitch length, how many seconds we want the note to sound when triggered
pitchLength = 1

# neopixel brightness
pixelBrightness = 0.05

# the number of samples taken per second in Hertz
SAMPLERATE = 8000

# how many samples we're collecting
NUM_SAMPLES = 160 

# set up note values in Hz. Find frequency values at https://pages.mtu.edu/~suits/notefreqs.html
Ab3 = 208
A3 = 223
As3 = 233
Bb3 = 233
B3 = 247
C4 = 262
Cs4 = 277
Db4 = 277
D4 = 294
Ds4 = 311
Eb4 = 311
E4 = 330
F4 = 349
Fs4 = 370
Gb4 = 370
G4 = 392
Gs4 = 415




#set up the neopixels

pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness= pixelBrightness) #determine beightness (Value can be between 0 and 1)



#
#
#
# Program the two buttons on the board to be able to move up and down pitches
#
#
#

buttonD = DigitalInOut(board.BUTTON_A) #button a is the down button
buttonD.direction = Direction.INPUT
buttonD.pull = Pull.DOWN

buttonU = DigitalInOut(board.BUTTON_B) # button b is the up button
buttonU.direction = Direction.INPUT
buttonU.pull = Pull.DOWN




#
#
#
# enable the speaker
#
#
#

spkrenable = DigitalInOut(board.SPEAKER_ENABLE)
spkrenable.direction = Direction.OUTPUT
spkrenable.value = True






#
#
#
#Taking and analyzing input from the microphone (The hard part...)
#This block of code will essentially allow us to find the magnitude or loudness of the mic input (Your breath!)
#
#
#



# Prep a buffer to record into



# For CircuitPython 2.x:

mic = audiobusio.PDMIn(board.MICROPHONE_CLOCK, board.MICROPHONE_DATA, frequency=16000, bit_depth=16)

# For Circuitpython 3.0 and up, "frequency" is now called "sample_rate".
# Comment the lines above and uncomment the lines below.
#mic = audiobusio.PDMIn(board.MICROPHONE_CLOCK, board.MICROPHONE_DATA,
#                       sample_rate=16000, bit_depth=16)

samples = array.array('H', [0] * NUM_SAMPLES)



# Remove DC bias before computing RMS.
def normalized_rms(values):
    minbuf = int(mean(values))
    return math.sqrt(sum(float((sample - minbuf) * (sample - minbuf)) for sample in values) / len(values))

def mean(values):
    return (sum(values) / len(values))









#Create a counter for tracking button presses
#Declared outside scope of while loop so it doesn't get reset to 0 at the beginnning of every loop!

counter = 0



#While loop that loops on forever
#
#This is where the real program functionality runs!

while True:

    #We begin regcording samples from the board's mic
    mic.record(samples, len(samples))
    magnitude = normalized_rms(samples)  
    print("mag = ", magnitude) #print the magnitude of the input blowing so we can track values in the serial console
    
    
    #If statements to know when up or down buttons are pushed
    #We will use a counter to track which pitch is selected
    
    if buttonU.value == True:  # If Up button is pushed then move up a pitch
        pixels.fill((0, 0, 0)) #turn all neopixels off
        counter += 1 #increase the counter by 1
        time.sleep(debounceTime) #to ensure button isn't triggered multiple times in one press we must "debounce" the button by creating a short delay after pressing it
    elif buttonD.value == True: #Do the same for the down button
        pixels.fill((0, 0, 0)) # If Down button is pushed then move down a pitch
        counter -= 1 #decrease counter by one
        time.sleep(debounceTime) #debounce button
        
        
    #If statements for determine which pitch the board is on
    #We will use the current counter value to set which frequency, neopixel, and color should be selected

    if counter == 0:  # Ab
        pixels[9] = (0, 0, 255)
        FREQUENCY = Ab3
    elif counter == 1:  # A
        pixels[9] = (0, 255, 0)
        FREQUENCY = A3
    elif counter == 2:  # A#
        pixels[9] = (255, 0, 0)
        FREQUENCY = As3
    elif counter == 3:  # Bb
        pixels[0] = (0, 0, 255)
        FREQUENCY = Bb3
    elif counter == 4:  # B
        pixels[0] = (0, 255, 0)
        FREQUENCY = B3
    elif counter == 5:  # C
        pixels[1] = (0, 255, 0)
        FREQUENCY = C4
    elif counter == 6:  # C#
        pixels[1] = (255, 0, 0)
        FREQUENCY = Cs4
    elif counter == 7:  # Db
        pixels[2] = (0, 0, 255)
        FREQUENCY = Db4
    elif counter == 8:  # D
        pixels[2] = (0, 255, 0)
        FREQUENCY = D4
    elif counter == 9:  # D#
        pixels[2] = (255, 0, 0)
        FREQUENCY = Ds4
    elif counter == 10:  # Eb
        pixels[3] = (0, 0, 255)
        FREQUENCY = Eb4
    elif counter == 11:  # E
        pixels[3] = (0, 255, 0)
        FREQUENCY = E4
    elif counter == 12:  # F
        pixels[4] = (0, 255, 0)
        FREQUENCY = F4
    elif counter == 13:  # F#
        pixels[4] = (255, 0, 0)
        FREQUENCY = Fs4
    elif counter == 14:  # Gb
        pixels[5] = (0, 0, 255)
        FREQUENCY = Gb4
    elif counter == 15:  # G
        pixels[5] = (0, 255, 0)
        FREQUENCY = G4
    elif counter == 16:  # G#
        pixels[5] = (255, 0, 0)
        FREQUENCY = Gs4
    elif counter > 16:  # if counter goes above 16 set back to 0
        counter = 0
    elif counter < 0:  # if counter goes below 0 set back to 16
        counter = 16





    #If statement to trigger pitch when user blows into mic
    #We will say that on a any loud sound the pitch is triggered
    
    if magnitude > blowThresshold: #any time we get a sound with a magnitude greater than the value of blowThresshold, trigger the current pitch (can be changed at top where it is defined)
        length = SAMPLERATE // FREQUENCY #create length of sample
        sine_wave = array.array("H", [0] * length) #create an array for a sine wave
        for i in range(length):
            sine_wave[i] = int(math.sin(math.pi * 2 * i / 18) * (2 ** 15) + 2 ** 15) #fill the array with values
        
        # For CircuitPython 2.x:
        
        sample = audioio.AudioOut(board.SPEAKER, sine_wave)
        sample.frequency = SAMPLERATE
        sample.play(loop=True)  # Play the sample
        time.sleep(pitchLength)  # Play for length of pitchLength
        sample.stop()  # we tell the board to stop
        
        # For Circuitpython 3.0 and up, comment above code and uncomment below
        
        #audio = audioio.AudioOut(board.SPEAKER)
        #sine_wave_sample = audioio.RawSample(sine_wave)
        #audio.play(sine_wave_sample, loop=True)  # Play the sample
        #time.sleep(pitchLength)  # Play for length of pitchLength
        #audio.stop()  # we tell the board to stop
        #audio.deinit()

    pixels.show() #show the desired neopixel light up on board 


#End program!!!