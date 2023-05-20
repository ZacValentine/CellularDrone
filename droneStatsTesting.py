weight = 3.0  # kg
#thrust = 19.6  # N (2 kgF)
thrust = 9.8 # N (1 kgF) (50% power for 12$ - 50$ motors)
density = 1.225  # kg/m^3 (air density at sea level)

displayNegativeAccel = False


wingWidth = 0.33 # m (1ft)

wingThickness = 0.05 # m (2 inches)

#Varying data
minWingSpan = .5 # m (1.5 ft to 9 ft)
maxWingSpan = 3
# calculate number of iterations for wingspan, and how much to increment by
wingSpanSteps = int(maxWingSpan/minWingSpan)
wingSpanStepSize = (maxWingSpan - minWingSpan) / (wingSpanSteps - 1)

minVelocity = 2 # m/s
maxVelocity = 12
# calculate number of iterations for velocity, and how much to increment by
velocitySteps = int(maxVelocity/minVelocity)
velocityStepSize = (maxVelocity - minVelocity) / (velocitySteps - 1)
# velocitySteps = 4
# velocityStepSize = 2

for i in range(wingSpanSteps):

    # increment wingspan for and set wingspan dependent data
    wingSpan = minWingSpan + (i * wingSpanStepSize) # m
    wingArea = wingSpan * wingWidth # m^2
    crossSection = wingSpan * wingThickness # m^2 (front view)

    print("wingSpan:", wingSpan, "m  wingArea:", wingArea, "m^2  wingWidth:", wingWidth, "m  wingThickness:", wingThickness, "m  weight:", weight, "kg  thrust:", thrust, "N")

    gravity = weight * -9.8

    for i in range(velocitySteps):

        # increment velocity for new data
        velocity = minVelocity + velocityStepSize * i

        # calculate lift and drag with incremented variables
        lift = 0.5 * density * wingArea * 1.5 * (velocity * velocity)
        drag = 0.5 * density * crossSection * 1 * (velocity * velocity)

        if(thrust - drag < 0 and not displayNegativeAccel):
            print("velocity", float(f'{velocity:.2f}'), "m/s    SPEED WILL NEVER BE REACHED -- FORWARD ACCELERATION IS NEGAVTIVE")
        else:
            print("velocity", float(f'{velocity:.2f}'), "m/s    lift:", float(f'{lift:.2f}'), "N    lift after gravity:", float(f'{lift + gravity:.2f}'), "N    upward acceleration at velocity:", float(f'{(lift + gravity) / weight:.2f}'), "m/s^2    drag:", float(f'{drag:.2f}'), "N    thrust after drag", float(f'{thrust - drag:.2f}'), "N     forward acceleration at velocity:", float(f'{(thrust - drag) / weight:.2f}'), "m/s^2")
    print()

