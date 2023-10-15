# import modules from Pyfirmata
from pyfirmata import Arduino, INPUT , OUTPUT, util
#import inbuilt time module
import time
import sys

print("_ _ _ _ _ _ _ _ _ _ _ _")
print("Morse Code Transceiver")
print("_ _ _ _ _ _ _ _ _ _ _ _")
print()

begin=input("Select the device mode Transmitter (T), Receiver(R) - ")

if begin == "T" :

    print("_ _ _ _ _ _ _ _ _ _ _ _")
    print("Morse Code Transmitter")
    print("_ _ _ _ _ _ _ _ _ _ _ _")
    print()

    
    DICTIONARY = {'A': '.-', 'B': '-...',
                  'C': '-.-.', 'D': '-..', 'E': '.',
                  'F': '..-.', 'G': '--.', 'H': '....',
                  'I': '..', 'J': '.---', 'K': '-.-',
                  'L': '.-..', 'M': '--', 'N': '-.',
                  'O': '---', 'P': '.--.', 'Q': '--.-',
                  'R': '.-.', 'S': '...', 'T': '-',
                  'U': '..-', 'V': '...-', 'W': '.--',
                  'X': '-..-', 'Y': '-.--', 'Z': '--..',
                  '1': '.----', '2': '..---', '3': '...--',
                  '4': '....-', '5': '.....', '6': '-....',
                  '7': '--...', '8': '---..', '9': '----.',
                  '0': '-----', ', ': '--..--', '.': '.-.-.-',
                  '?': '..--..', '/': '-..-.', '-': '-....-',
                  '(': '-.--.', ')': '-.--.-',
                  'a': '.-', 'b': '-...',
                  'c': '-.-.', 'd': '-..', 'e': '.',
                  'f': '..-.', 'g': '--.', 'h': '....',
                  'i': '..', 'j': '.---', 'k': '-.-',
                  'l': '.-..', 'm': '--', 'n': '-.',
                  'o': '---', 'p': '.--.', 'q': '--.-',
                  'r': '.-.', 's': '...', 't': '-',
                  'u': '..-', 'v': '...-', 'w': '.--',
                  'x': '-..-', 'y': '-.--', 'z': '--..', ' ': ' '} # from wikipedia
    
    # create an Arduino board instance
    board = Arduino('COM22')
    # digital pin number
    led_pin = 7
    #buzzer = board.get_pin('d:9:p')
    
    unit_time_interval = 0.2  # From wikipedia unit time interval for Morse code
    
    text = input("Enter a string to transmit : ")
    
    it = util.Iterator(board)
    it.start()
    
    #print(' '.join([DICT[i] for i in txt]))
    board.digital[led_pin].mode = OUTPUT


    def str_morse(string):
        for char in string:
                                        
            if char == '.':
                board.digital[led_pin].write(1)
                #buzzer.write(0.9)
                time.sleep(unit_time_interval) # short mark, dot or "dit": one time unit long
                board.digital[led_pin].write(0)
                #buzzer.write(0)
                time.sleep(unit_time_interval) #inter-element gap between the dots and dashes within a character: one dot duration or one unit long

            elif char == '-':
                board.digital[led_pin].write(1)
                #buzzer.write(0.9)
                time.sleep(3 * unit_time_interval) # longer mark, dash or "dah": three time units long
                board.digital[led_pin].write(0)
                #buzzer.write(0)
                time.sleep(unit_time_interval) # inter-element gap between the dots and dashes within a character: one dot duration or one unit long
                
            elif char == ' ':
                time.sleep(7 * unit_time_interval) # medium gap (between words): seven time units long
                
        time.sleep(3 * unit_time_interval) # short gap (between letters): three time units long


    morse = [DICTIONARY[i] for i in text]
    
    for i in morse:
        print(i, end=' ')
        str_morse(i)

elif begin == "R" :
    
    print("_ _ _ _ _ _ _ _ _ _ _ _")
    print("Morse Code Receiver")
    print("_ _ _ _ _ _ _ _ _ _ _ _")
    print()

    
    DICTIONARY = {'1': '.----', '2': '..---', '3': '...--',
                  '4': '....-', '5': '.....', '6': '-....',
                  '7': '--...', '8': '---..', '9': '----.',
                  '0': '-----', ', ': '--..--', '.': '.-.-.-',
                  '?': '..--..', '/': '-..-.', '-': '-....-',
                  '(': '-.--.', ')': '-.--.-',
                  'a': '.-', 'b': '-...',
                  'c': '-.-.', 'd': '-..', 'e': '.',
                  'f': '..-.', 'g': '--.', 'h': '....',
                  'i': '..', 'j': '.---', 'k': '-.-',
                  'l': '.-..', 'm': '--', 'n': '-.',
                  'o': '---', 'p': '.--.', 'q': '--.-',
                  'r': '.-.', 's': '...', 't': '-',
                  'u': '..-', 'v': '...-', 'w': '.--',
                  'x': '-..-', 'y': '-.--', 'z': '--..', ' ': ' '} # from wikipedia
    
    # initial configurations
    board = Arduino("COM20")
    ldr_pin = 0
    space = 20
    board.analog[ldr_pin].mode = INPUT
    
    # start the utilization service
    # this service will handle communication overflows while communicating with the Arduino board via USB interface
    it = util.Iterator(board)
    it.start()
    
    board.analog[ldr_pin].enable_reporting()
    
    mor_string = ''


    def morse2str(morse):
        return list(DICTIONARY.keys())[list(DICTIONARY.values()).index(morse)]

    h_value = 0  # variable for LED OFF
    l_value = 0  # Variable for LED ON
    dec = 0.3 # Adujusted from values (from LDR)
    
    while True:
        
        ldrvalue = board.analog[ldr_pin].read()  # read the value
        #print(ldrvalue)
        time.sleep(0.01)
        
        if ldrvalue == None:
            continue
        
        if ldrvalue < dec:
            l_value += 1
            
            if 40 < h_value < 100: # 0.01*20*3=0.60 for ''/light OFF
                h_value = 0
                print(morse2str(mor_string), end='')
                mor_string = ''
                
            elif 120 < h_value < 200: # 0.01*20*7=1.40 for ' '/light OFF
                print(morse2str(mor_string), end='')
                print(' ', end='')
                mor_string = ''
                h_value = 0
                
            h_value = 0
            
        else:
            h_value += 1
            
            if l_value != 0 and l_value < 25: # 0.01*20=0.2 for '.'/light ON
                mor_string += '.'
                l_value = 0
                
            elif l_value > 25: # 0.01*20*3=0.6 for '-' /light ON
                mor_string += '-'
                l_value = 0
                
            if h_value > 200 and mor_string != '': # 200*0.01= 2 seconds/long time period without light end the code
                print(morse2str(mor_string))
                break

    
