function sysCall_init()
    visionSensor=simGetObjectHandle('Vision_sensor') -- nome do sensor
end

function sysCall_sensing()
  local image=simGetVisionSensorCharImage(visionSensor) -- Visão com baixa resolução (pixel 1x1) 
	local redPixel=image:byte(1) -- Valores em escala RGB: [0-173]
	local greenPixel=image:byte(2)
	local bluePixel=image:byte(3)
  print(redPixel, greenPixel, bluePixel )
end
