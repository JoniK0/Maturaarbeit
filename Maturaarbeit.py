from stockfish import Stockfish
import time
import board
from adafruit_motor import stepper
from adafruit_motorkit import MotorKit
import RPi.GPIO as GPIO

Relay_Ch1 = 26
Relay_Ch2 = 20
Relay_Ch3 = 21

GPIO.setup(Relay_Ch1,GPIO.OUT)
GPIO.setup(Relay_Ch2,GPIO.OUT)
GPIO.setup(Relay_Ch3,GPIO.OUT)

GPIO.output(Relay_Ch1, GPIO.HIGH)

stockfish = Stockfish()#path="../stockfish_15.1_linux_x64/stockfish-ubuntu-20.04-x86-64")

{
    "Debug Log File": "",
    "Contempt": 0,
    "Min Split Depth": 0,
    "Threads": 1, # More threads will make the engine stronger, but should be kept at less than the number of logical processors on your computer.
    "Ponder": "false",
    "Hash": 256, # Default size is 16 MB. It's recommended that you increase this value, but keep it as some power of 2. E.g., if you're fine using 2 GB of RAM, set Hash to 2048 (11th power of 2).
    "MultiPV": 1,
    "Skill Level": 20,
    "Move Overhead": 10,
    "Minimum Thinking Time": 20,
    "Slow Mover": 100,
    "UCI_Chess960": "false",
    "UCI_LimitStrength": "false",
    "UCI_Elo": 1350
}

stockfish.update_engine_parameters({"Hash": 32, "Minimum Thinking Time": 2})
#stockfish.set_depth(10)

kit = MotorKit(i2c=board.I2C())
OneSquare = 384


#halfsquares
def step(squares, direction):
        if direction == "up":
            for i in range((squares*OneSquare)//2):
                
                kit.stepper2.onestep(style=stepper.DOUBLE)
                kit.stepper1.onestep(style=stepper.DOUBLE)
                
            time.sleep(0.3)
            
        elif direction == "down":
            for i in range((squares*OneSquare)//2):
                
                
                #
                kit.stepper2.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
                kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
            time.sleep(0.3)
            
        elif direction == "right":
            for i in range((squares*OneSquare)//2):
                kit.stepper2.onestep(style=stepper.DOUBLE)
                kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
                
            time.sleep(0.3)
            
        elif direction == "left":
            for i in range((squares*OneSquare)//2):
                kit.stepper2.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
                kit.stepper1.onestep(style=stepper.DOUBLE)
                
            time.sleep(0.3)
        
            


def move(move):
     
    
    if move[0] == "a":
            x1 = 0
    elif move[0] == "b":
            x1 = 1
    elif move[0] == "c":
            x1 = 2
    elif move[0] == "d":
            x1 = 3
    elif move[0] == "e":
            x1 = 4
    elif move[0] == "f":
            x1 = 5
    elif move[0] == "g":
            x1 = 6
    elif move[0] == "h":
            x1 = 7
            
            
    if move[1] == "1":
            y1 = 0
    elif move[1] == "2":
            y1 = 1
    elif move[1] == "3":
            y1 = 2
    elif move[1] == "4":
            y1 = 3
    elif move[1] == "5":
            y1 = 4
    elif move[1] == "6":
            y1 = 5
    elif move[1] == "7":
            y1 = 6
    elif move[1] == "8":
            y1 = 7
   
   
   
    if move [2] == "a":
            x2 = 0
    elif move [2] == "b":
            x2 = 1
    elif move [2] == "c":
            x2 = 2
    elif move [2] == "d":
            x2 = 3
    elif move [2] == "e":
            x2 = 4
    elif move [2] == "f":
            x2 = 5
    elif move [2] == "g":
            x2 = 6
    elif move [2] == "h":
            x2 = 7
            
            
    if move[3] == "1":
            y2 = 0
    elif move[3] == "2":
            y2 = 1
    elif move[3] == "3":
            y2 = 2
    elif move[3] == "4":
            y2 = 3
    elif move[3] == "5":
            y2 = 4
    elif move[3] == "6":
            y2 = 5
    elif move[3] == "7":
            y2 = 6
    elif move[3] == "8":
            y2 = 7
         
    #step to the first square     
    
    step(x1*2, "right")
       
    ##for i in range(x1*OneSquare):
    ##    kit.stepper1.onestep()
    ##    kit.stepper2.onestep()
    
    step(y1*2, "up")
    
    ##for i in range(y1*OneSquare):
    ##    kit.stepper1.onestep()
    ##   kit.stepper2.onestep(direction=stepper.BACKWARD)
    
    
    ##electromagnet activates
    GPIO.output(Relay_Ch1, GPIO.LOW)
    ##
    
    vectorX = x2 - x1
    vectorY = y2 - y1
    
    #step half a square back if x stepping is required
    if vectorX != 0:
        
        step(1, "down")
        
        ##for i in range(OneSquare/2):
        ##    kit.stepper1.onestep(direction=stepper.BACKWARD)
        ##    kit.stepper2.onestep()
    
    #if x direction positive move to the right with vectorX
    #else move to the left with vectorX
    if vectorX >= 0:
        
        step(vectorX*2, "right")
        
        ##for i in range(vectorX*OneSquare):
        ##    kit.stepper1.onestep()
        ##    kit.stepper2.onestep()
            
    else:
        
        step((-vectorX*2), "left")
        
        ##for i in range(VectorX*OneSquare):
        ##   kit.stepper1.onestep(direction=stepper.BACKWARD)
        ##   kit.stepper2.onestep(direction=stepper.BACKWARD)
    
    #step half a square to the right if y stepping is required
    if vectorY != 0:
        
        step(1, "right")
        
        ##for i in range(OneSquare/2):
        ##    kit.stepper1.onestep()
        ##    kit.stepper2.onestep()
    
    #if y is positive move up
    #else move down
    if vectorY >= 0:
        
        step(vectorY*2, "up")
        
        ##for i in range(vectorY*OneSquare):
        ##    kit.stepper1.onestep()
        ##    kit.stepper2.onestep(direction=stepper.BACKWARD)
            
    else:
        
        step((-vectorY)*2, "down")
        
        ##for i in range(vectorY*OneSquare):
        ##    kit.stepper1.onestep(direction=stepper.BACKWARD)
        ##    kit.stepper2.onestep()
            
   
    
    # if we moved half a square down correct that back
    if vectorX != 0:
        
        step(1, "up")
        
        ##for i in range(OneSquare/2):
        ##    kit.stepper1.onestep()
        ##    kit.stepper2.onestep(direction=stepper.BACKWARD)
            
    #if we moved half a square to the right correct back
    if vectorY != 0:
        
        step(1, "left")
        
        ##for i in range(OneSquare/2):
        ##    kit.stepper1.onestep(direction=stepper.BACKWARD)
        ##    kit.stepper2.onestep(direction=stepper.BACKWARD)
    
    #deactivate electromagnet
    GPIO.output(Relay_Ch1, GPIO.HIGH)
    #
    
    
    #move to starting position
     
    step(x2*2, "left") 
     
    ##for i in range(OneSquare*x2):
    ##    kit.stepper1.onestep(direction=stepper.BACKWARD)
    ##    kit.stepper2.onestep(direction=stepper.BACKWARD)
       
    step(y2*2, "down")   
       
    ##for i in range(OneSquare*y2):
    ##    kit.stepper1.onestep(direction=stepper.BACKWARD)
    ##    kit.stepper2.onestep()
    
    #de-energise stepper motors so they don't get too hot
    kit.stepper1.release()
    kit.stepper2.release()
        
    
            
def takes(take):
        
    if take[0] == "a":
            x1 = 0
    elif take[0] == "b":
            x1 = 1
    elif take[0] == "c":
            x1 = 2
    elif take[0] == "d":
            x1 = 3
    elif take[0] == "e":
            x1 = 4
    elif take[0] == "f":
            x1 = 5
    elif take[0] == "g":
            x1 = 6
    elif take[0] == "h":
            x1 = 7
            
            
    if take[1] == "1":
            y1 = 0
    elif take[1] == "2":
            y1 = 1
    elif take[1] == "3":
            y1 = 2
    elif take[1] == "4":
            y1 = 3
    elif take[1] == "5":
            y1 = 4
    elif take[1] == "6":
            y1 = 5
    elif take[1] == "7":
            y1 = 6
    elif take[1] == "8":
            y1 = 7
   
   
   
    if take [2] == "a":
            x2 = 0
    elif take [2] == "b":
            x2 = 1
    elif take [2] == "c":
            x2 = 2
    elif take [2] == "d":
            x2 = 3
    elif take [2] == "e":
            x2 = 4
    elif take [2] == "f":
            x2 = 5
    elif take [2] == "g":
            x2 = 6
    elif take [2] == "h":
            x2 = 7
            
            
    if take[3] == "1":
            y2 = 0
    elif take[3] == "2":
            y2 = 1
    elif take[3] == "3":
            y2 = 2
    elif take[3] == "4":
            y2 = 3
    elif take[3] == "5":
            y2 = 4
    elif take[3] == "6":
            y2 = 5
    elif take[3] == "7":
            y2 = 6
    elif take[3] == "8":
            y2 = 7
    
    #step to the piece that will be taken
    
    step(x2*2, "right")
    step(y2*2, "up")
    
    #activate electromagnet
    
    #
    
    #discard piece
    
    step(1, "down")
    step((8*2)-x2, "right")
    step(1, "up")
    
    #deactivate electromagnet
    
    #
    
    #step back to x2,y2
    step((8*2)-x2, "left")
    
    vectorX = x1 - x2
    vectorY = y1 - y2
    
    
    #step to x1,y1
    if vectorX >= 0:
        step(2*vectorX, "right")
        
    else:
        step(2*(-vectorX), "left")
        
    if vectorY >= 0:
        step(2*vectorY, "up")
        
    else:
        step(2*(-vectorY), "down")
        
    #activate electromagnet
    
    #
    
    #move the piece to x2,y2
    
    #x stepping
    if vectorX != 0:
        step(1, "down")
        
    if vectorX >= 0:
        step(2*(-vectorX), "right")
        
    else:
        step(2*vectorX, "left")
      
      
      # y stepping 
    if vectorY != 0:
        step(1, "right")
           
    if vectorY >= 0:
        
        step((-vectorY)*2, "up")

    else:
        
        step(vectorY*2, "down")
        
    #correction if needed
    
    if vectorX != 0:
        step(1, "up")
        
    if vectorY != 0:
        step(1, "left")
        
    #deactivate electromagnet
        
    #
    
    #go back to start
    step(x2*2, "left")
    step(y2*2, "down")
    
    
    #de-energise stepper motors so they don't get too hot
    kit.stepper1.release()
    kit.stepper2.release()
        
    
    
    
      
        
    
    
    
    
    
        
    
    
    

    


print("Difficulty(elo):")
elo = input()
Elo = int(elo)

stockfish.set_elo_rating(Elo)

while True:
    
    print("your move")
    MyMove=input()
 
     
    if stockfish.will_move_be_a_capture(MyMove) == Stockfish.Capture.DIRECT_CAPTURE:
        takes(MyMove)
         
    else:
        move(MyMove)
       
        
    stockfish.make_moves_from_current_position([MyMove])
    
    time.sleep(2)
    
    
    StockMove = stockfish.get_best_move_time(1000)

    if stockfish.will_move_be_a_capture(StockMove) == Stockfish.Capture.DIRECT_CAPTURE:
        takes(StockMove)
        print("capture!")
        
    else:
        move(StockMove)
        print("move!")
        
    kit.stepper1.release()
    kit.stepper2.release()

    stockfish.make_moves_from_current_position([StockMove])
    
    print(stockfish.get_board_visual())


