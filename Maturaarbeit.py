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
     
    shift = ord("a")
    
    x1 = ord(MyMove[0]) - shift
    y1 = int(MyMove[1]) - 1
    
    x2 = ord(MyMove[2]) - shift
    y2 = int(MyMove[3]) - 1
    #step to the first square     
    
    step(x1*2, "right")
       
    step(y1*2, "up")
    
    ##electromagnet activates
    GPIO.output(Relay_Ch1, GPIO.LOW)
    ##
    
    vectorX = x2 - x1
    vectorY = y2 - y1
    
    #step half a square back if x stepping is required
    if vectorX != 0:
        
        step(1, "down")

    
    #if x direction positive move to the right with vectorX
    #else move to the left with vectorX
    if vectorX >= 0:
        
        step(vectorX*2, "right")
            
    else:
        
        step((-vectorX*2), "left")
        
    #step half a square to the right if y stepping is required
    if vectorY != 0:
        
        step(1, "right")
    
    #if y is positive move up
    #else move down
    if vectorY >= 0:
        
        step(vectorY*2, "up")
        
    else:
        
        step((-vectorY)*2, "down")
    
    # if we moved half a square down correct that back
    if vectorX != 0:
        
        step(1, "up")
        
    #if we moved half a square to the right correct back
    if vectorY != 0:
        
        step(1, "left")
    
    #deactivate electromagnet
    GPIO.output(Relay_Ch1, GPIO.HIGH)
    #
    
    
    #move to starting position
     
    step(x2*2, "left") 
     
    step(y2*2, "down")   
    
    #de-energise stepper motors so they don't get too hot
    kit.stepper1.release()
    kit.stepper2.release()
        
    
            
def takes(take):
    shift = ord("a")
    
    x1 = ord(MyMove[0]) - shift
    y1 = int(MyMove[1]) - 1
    
    x2 = ord(MyMove[2]) - shift
    y2 = int(MyMove[3]) - 1
    
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

def Castle(color, side):
    
    if color == "black" and side == "short":
        step(4*2, "right")
        step(7*2, "up")
        GPIO.output(Relay_Ch1, GPIO.LOW)
        step(2*2, "right")
        GPIO.output(Relay_Ch1, GPIO.HIGH)
        step(2, "right")
        GPIO.output(Relay_Ch1, GPIO.LOW)
        step(1, "up")
        step(2*2, "left")
        step(1, "down")
        GPIO.output(Relay_Ch1, GPIO.HIGH)
        step(7*2, "down")
        step(4*2, "left")

    if color == "white" and side == "short":
        step(4*2, "right")
        GPIO.output(Relay_Ch1, GPIO.LOW)
        step(2*2, "right")
        GPIO.output(Relay_Ch1, GPIO.HIGH)
        step(2, "right")
        GPIO.output(Relay_Ch1, GPIO.LOW)
        step(1, "down")
        step(2*2, "left")
        step(1, "up")
        GPIO.output(Relay_Ch1, GPIO.HIGH)
        step(5*2, "left")
          


    if color == "black" and side == "long":
        step(4*2, "right")
        step(7*2, "up")
        GPIO.output(Relay_Ch1, GPIO.LOW)
        step(2*2, "left")
        GPIO.output(Relay_Ch1, GPIO.HIGH)
        step(2*2, "left")
        GPIO.output(Relay_Ch1, GPIO.LOW)
        step(1, "up")
        step(3*2, "right")
        step(1, "down")
        GPIO.output(Relay_Ch1, GPIO.HIGH)
        step(7*2, "down")
        step(3*2, "left")


    if color == "white" and side == "long":
        step(4*2, "right")
        GPIO.output(Relay_Ch1, GPIO.LOW)
        step(2*2, "left")
        GPIO.output(Relay_Ch1, GPIO.HIGH)
        step(2*2, "left")
        GPIO.output(Relay_Ch1, GPIO.LOW)
        step(1, "down")
        step(3*2, "right")
        step(1, "up")
        GPIO.output(Relay_Ch1, GPIO.HIGH)
        step(3*2, "left")

def passant(move):
    
    shift = ord("a")

    x1 = ord(move[0]) - shift
    y1 = int(move[1]) - 1

    x2 = ord(MyMove[2]) - shift
    y2 = int(MyMove[3]) - 1

    step(2*x1, "right")
    step(2*y1, "up")

    GPIO.output(Relay_Ch1, GPIO.LOW)
    
    step(1, "up")
    step((8*2)-x2, "right")
    step(1, "down")

    GPIO.output(Relay_Ch1, GPIO.HIGH)

    step((8*2) - x2, "left")

    x = x1 - x2

    if x > 0:
        step(2, "right")

    else:
        step(2, "left")

    GPIO.output(Relay_Ch1, GPIO.LOW)

    if x > 0:
        step(2, "left")

    else:
        step(2, "right")

    y = y2 - y1

    if y > 0:
        step(2, "up")

    else:
        step(2, "down")

    GPIO.output(Relay_Ch1, GPIO.HIGH)

    step(2*x2, "left")
    step(2*y2, "down")

    kit.stepper1.release()
    kit.stepper2.release()
        
print("Difficulty(elo):")
elo = input()
Elo = int(elo)

stockfish.set_elo_rating(Elo)

while True:
    
    print("your move")
    MyMove=input()
 
     
    while stockfish.is_move_correct(MyMove) == False:
        print("this is an invalid move")
        print("please insert a valid move:")
        MyMove = input()
        continue
    

    if stockfish.get_what_is_on_square("e1") == Stockfish.Piece.WHITE_KING and MyMove == "e1g1":
        print("castle")
        Castle("white", "short")

    elif stockfish.get_what_is_on_square("e1") == Stockfish.Piece.WHITE_KING and MyMove == "e1c1":
        print("longcastle")
        Castle("white", "long")
 
     
    elif stockfish.will_move_be_a_capture(MyMove) == Stockfish.Capture.DIRECT_CAPTURE:
        takes(MyMove)

    elif stockfish.will_move_be_a_capture(MyMove) == Stockfish.Capture.EN_PASSANT:
        passant(MyMove)
        print("en passant")
         
    else:
        move(MyMove)
       
        
    stockfish.make_moves_from_current_position([MyMove])
    
    time.sleep(2)
    
    
    StockMove = stockfish.get_best_move_time(1000)


    if stockfish.get_what_is_on_square("e8") == Stockfish.Piece.BLACK_KING and StockMove == "e8g8":
        print("castle")
        Castle("black", "short")

    elif stockfish.get_what_is_on_square("e8") == Stockfish.Piece.BLACK_KING and StockMove == "e8c8":
        print("longcastle")
        Castle("black", "long")

    elif stockfish.will_move_be_a_capture(StockMove) == Stockfish.Capture.DIRECT_CAPTURE:
        takes(StockMove)
        print("capture!")

    elif stockfish.will_move_be_a_capture(StockMove) == Stockfish.Capture.EN_PASSANT:
        passant(StockMove)
        
    else:
        move(StockMove)
        print("move!")
        
    kit.stepper1.release()
    kit.stepper2.release()

    stockfish.make_moves_from_current_position([StockMove])
    
    print(stockfish.get_board_visual())