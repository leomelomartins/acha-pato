"""acha_pato controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import *
from controller import Camera
from controller import CameraRecognitionObject

def run_robot(robot):
   
   # get the time step of the current world.
   timestep = int(robot.getBasicTimeStep())
   max_speed = 6.28
    
   #enable motors
   left_motor = robot.getDevice('left wheel motor')
   right_motor = robot.getDevice('right wheel motor')
   
   left_motor.setPosition(float('inf'))
   left_motor.setVelocity(0.0)
    
   right_motor.setPosition(float('inf'))
   right_motor.setVelocity(0.0)
   
   #enable camera
   on_camera = robot.getDevice('camera')
   on_camera.enable(timestep)
   on_camera.hasRecognition()
   on_camera.recognitionEnable(timestep)
    
   #Enable proximity sensors
   prox_sensors = []
   for ind in range(8):
       sensor_name = 'ps' + str(ind)
       prox_sensors.append(robot.getDevice(sensor_name))
       prox_sensors[ind].enable(timestep)
    
   flag = 0
    
   # Main loop:
   # - perform simulation steps until Webots is stopping the controller
   while robot.step(timestep) != -1:
     
       # Process sensor data here
       left_wall = prox_sensors[5].getValue() > 80
       left_corner = prox_sensors[6].getValue() > 80
       front_wall = prox_sensors[7].getValue() > 80
       
       left_speed = max_speed
       right_speed = max_speed
       
       #Image object recognition
       if on_camera.getRecognitionNumberOfObjects():
           cameraObjs = on_camera.getRecognitionObjects()
           for obj in cameraObjs:
               color = obj.get_colors()
               if ((color[0] > 0.8) & (color[1] > 0.7) & (color[2] < 0.2)):
                   print("ACHEI O PATINHO! NICE")
                   if flag == 0:
                       flag = 1                 
               
               else:
                   print("NÃO É O PATINHO! GRRR")
          
       if (flag == 0) | (flag < 20):
           if (flag != 0):
               flag += 1
           
           if front_wall:
               left_speed = max_speed
               right_speed = -max_speed
               
           else:
           
               if left_wall:
                   left_speed = max_speed
                   right_speed = max_speed
                   
               else:
                   left_speed = max_speed/8
                   right_speed = max_speed
                   
               if left_corner:
                   left_speed = max_speed
                   right_speed = max_speed/8
              
                
       elif (flag == 20):
           left_motor.setVelocity(0)
           right_motor.setVelocity(0) 
           on_camera.saveImage('achei_patinho.png', 100)
           return
                     
       # Enter here functions to send actuator commands, like:
       left_motor.setVelocity(left_speed)
       right_motor.setVelocity(right_speed)


# Enter here exit cleanup code.
if __name__ == "__main__":
       
       #create robot instance
       my_robot = Robot()
       run_robot(my_robot)