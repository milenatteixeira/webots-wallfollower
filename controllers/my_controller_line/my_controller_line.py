from controller import Robot

def run_robot(robot):
    time_step = 64
    max_speed = 6.28
    cont = 0

    end_cont = {64: 15, 128: 8}

    passedFirstRight = False

    #configuração dos motores
    left_motor = robot.getDevice('left wheel motor')
    right_motor = robot.getDevice('right wheel motor')
    left_motor.setPosition(float('inf'))
    right_motor.setPosition(float('inf'))
    left_motor.setVelocity(0.0)
    right_motor.setVelocity(0.0)

    #configuração dos sensores de distancia
    sensor_prox = []
    for i in range(8):
        sensor_prox.append(robot.getDevice(f'ps{i}'))
        sensor_prox[i].enable(time_step)
    
    while robot.step(time_step) != -1:
        for i in range(8):
            print(f'sensor {i}: {sensor_prox[i].getValue()}')

        left_wall = sensor_prox[5].getValue() > 80
        left_corner = sensor_prox[6].getValue() > 80
        front_wall = sensor_prox[7].getValue() > 80
        first_right = sensor_prox[2].getValue() > 80
        
        if passedFirstRight:
            first_right = False
        
        print(f'Left: {left_wall}; Front: {front_wall}; Right: {cont}')

        left_speed = max_speed
        right_speed = max_speed

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
            if left_corner or first_right:
                if first_right:
                    cont += 1
                    if cont >= end_cont.get(time_step):
                        passedFirstRight = True
                left_speed = max_speed
                right_speed = max_speed/8

        left_motor.setVelocity(left_speed)
        right_motor.setVelocity(right_speed)

if __name__ == "__main__":
    my_robot = Robot()
    run_robot(my_robot)
