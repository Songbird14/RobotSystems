import picarx_improved

px = picarx_improved.Picarx()

keep_going = True
while keep_going:
    val = input("Enter your choice of maneuver: ")
    val = int(val)
    if val == 1:
        print('IN')
        speed = int(input("Enter speed: "))
        angle = int(input("Enter angle (for straight put 0): "))
        px.move_forward(speed,angle)

    elif val == 2:
        speed = int(input("Enter speed: "))
        angle = int(input("Enter angle (for straight put 0): "))
        px.move_backward(speed,angle)

    elif val == 3: 
        px.parallel_park()

    elif val == 4: 
        px.k_turn()
    
    elif val == 0:
        keep_going = False
    else: 
        print('Invalid command. Try again')