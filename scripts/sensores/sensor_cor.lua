function sysCall_init()
    visionSensor=simGetObjectHandle('Vision_sensor') -- nome do sensor
    BLACK = 0
    RED = 1
    YELLOW = 2
    GREEN = 3
    BLUE = 4
    WHITE = 5
end

function getColorSensor(sensor)
    local image=simGetVisionSensorCharImage(visionSensor)  -- Visão com baixa resolução (pixel 1x1) 
    local redPixel=image:byte(1) -- Valores em escala RGB: [0-173]
    local greenPixel=image:byte(2)
    local bluePixel=image:byte(3)
    local minColor = 150
    local red, green, blue, colorRGB
    red = 0
    green = 0
    blue = 0
    if (redPixel > minColor) then 
        red = 1
    end
    if (greenPixel > minColor) then 
        green = 10
    end
    if (bluePixel > minColor) then 
        blue = 100
    end
    colorRGB = red + green + blue
    if     (colorRGB == 0) then return BLACK
    elseif (colorRGB == 1) then return RED
    elseif (colorRGB == 11) then return YELLOW
    elseif (colorRGB == 10) then return GREEN
    elseif (colorRGB == 100) then return BLUE
    elseif (colorRGB == 111) then return BLACK
    end
end

function sysCall_sensing()
    print(getColorSensor(visionSensor))
end
