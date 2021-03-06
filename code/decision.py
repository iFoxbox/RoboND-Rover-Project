import numpy as np


#create a reusable stop function
def trigger_stop(Rover): 
    # Set mode to "stop" and hit the brakes!
    Rover.throttle = 0
    # Set brake to stored brake value
    Rover.brake = Rover.brake_set
    Rover.steer = 0
    Rover.next_mode = 'stop'
    
   
        

        
# This is where you can build a decision tree for determining throttle, brake and steer 
# commands based on the output of the perception_step() function
def decision_step(Rover):

    # Check if we have vision data to make decisions with
    if Rover.nav_angles is not None:
        
        # Check for Rover.mode status
        if Rover.mode =='retreaving':
            if len(Rover.rock_angles) >= Rover.stop_forward:  
                # If rock is forward navigate to it
                # and velocity is below max, then throttle 
                if Rover.vel < Rover.max_vel /2:
                    # Set throttle value to throttle setting
                    Rover.throttle = Rover.throttle_set
                else: # Else coast
                    Rover.throttle = 0
                Rover.brake = 0
            #steer to rock     
            Rover.steer = np.clip(np.mean(Rover.rock_angles * 180/np.pi), -15, 15) 
            if (len(Rover.nav_angles) < Rover.stop_forward) or Rover.near_sample:
                   trigger_stop(Rover)
                    
            
        if Rover.mode == 'forward': 
            # Check the extent of navigable terrain
            if len(Rover.nav_angles) >= Rover.stop_forward:  
                # If mode is forward, navigable terrain looks good 
                # and velocity is below max, then throttle 
                if Rover.vel < Rover.max_vel:
                    # Set throttle value to throttle setting
                    Rover.throttle = Rover.throttle_set
                else: # Else coast
                    Rover.throttle = 0
                Rover.brake = 0
           
                # Set steering to average angle clipped to the range +/- 15
                Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi), -15, 15)
                    
            # If there's a lack of navigable terrain pixels then go to 'stop' mode
            elif (len(Rover.nav_angles) < Rover.stop_forward) or Rover.near_sample:
                trigger_stop(Rover)
            
                
        # If we're already in "stop" mode then make different decisions
        elif Rover.mode == 'stop':
            # If we're in stop mode but still moving keep braking
            if Rover.vel > 0.2:
                Rover.throttle = 0
                Rover.brake = Rover.brake_set
                Rover.steer = 0
            # If we're not moving (vel < 0.2) then do something else
            elif Rover.vel <= 0.2:
                # Now we're stopped and we have vision data to see if there's a path forward
                Rover.brake = 0
                if (not (-10 <= np.mean(Rover.nav_angles * 180/np.pi)<= 10)) and (len(Rover.nav_angles) < Rover.go_forward):
                    Rover.throttle = 0
                    # Release the brake to allow turning
                    Rover.brake = 0
                   
                # Turn range is +/- 15 degrees, when stopped the next line will induce 4-wheel turning
                Rover.steer = +15 
                    
                        
                if len(Rover.nav_angles) >= Rover.go_forward:
                    # Set throttle back to stored value
                    Rover.throttle = Rover.throttle_set
                    # Release the brake
                    Rover.brake = 0
                    # Set steer to mean angle
                    Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi), -15, 15)
                    Rover.next_mode = 'forward'
    
                #If a sample is pressent set grab flag 
                if Rover.near_sample: 
                    Rover.send_pickup = True
                else: 
                    Rover.send_pickup = False
                # If we're stopped but see sufficient navigable terrain in front then go!
                
    else:
        Rover.throttle = Rover.throttle_set
        Rover.steer = 0
        Rover.brake = 0
        
    # If in a state where want to pickup a rock send pickup command
    if Rover.near_sample and Rover.vel == 0 and not Rover.picking_up:
        Rover.send_pickup = True
    
    return Rover

