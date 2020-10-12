function moveForward()
    sim.setJointTargetVelocity(front_r_wheel,0.5*max_speed/wheel_radius)
    sim.setJointTargetVelocity(front_l_wheel,0.5*max_speed/wheel_radius)
end
 
function moveBackward()
    sim.setJointTargetVelocity(front_r_wheel,-0.5*max_speed/wheel_radius)
    sim.setJointTargetVelocity(front_l_wheel,-0.5*max_speed/wheel_radius)
end
 
function turnLeft()
    sim.setJointTargetVelocity(front_r_wheel,0.5*max_speed/wheel_radius)
    sim.setJointTargetVelocity(front_l_wheel,-0.5*max_speed/wheel_radius)
end
 
function turnRight()
    sim.setJointTargetVelocity(front_r_wheel,-0.5*max_speed/wheel_radius)
    sim.setJointTargetVelocity(front_l_wheel,0.5*max_speed/wheel_radius)
end
 
 
 
function sysCall_init()
    -- do some initialization here
    front_r_wheel=sim.getObjectHandle('Revolute_joint')
    front_l_wheel=sim.getObjectHandle('Revolute_joint0')
    wheel_radius=0.025
    max_speed=0.05
end
 
function sysCall_actuation()
    -- put your actuation code here
 
 
end
 
function sysCall_sensing()
    -- put your sensing code here
end
 
function sysCall_cleanup()
    -- do some clean-up here
end
 
-- See the user manual or the available code snippets for additional callback functions and details
 