
from .Thermal_box import Box


def main():
    print("hallo World")
    combustion_chamber = Box(1,2,3)
    print(f"The gas of the mass of the combustion chamber is: {combustion_chamber.mass:.2f} kg")


    #dummy heat source
    Q = 10 #W


    #Maximum number of iterations
    ite = 100
    # Initialize the while counter
    i = 0
    # set the time step
    dt = 1 #s
    #simulation loop starts here
    while i < ite:
        i += 1
        combustion_chamber.heat_addtion(1000,dt)


    print(combustion_chamber.temperature)
    print(combustion_chamber.pressure)


main()
