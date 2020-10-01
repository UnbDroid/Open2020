function sysCall_init()
    IR = sim.getObjectHandle('IR_sensor') -- nome do sensor
    max_distance_IR = 1
end

function getDistanceIR(sensor)
    local detectable, distance, dp
    detectable, distance, dp =sim.checkProximitySensor(sensor,sim.handle_all)
    if(detectable == 0) then
        distance = max_distance_IR
    end
    return distance
end
