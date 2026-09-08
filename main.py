
from Thermal_box import Box
from Orifice_plate import Plate
from Orifice_plate import save_plate_png


def main():
    #------- MAke the computational domain ------
    combustion_chamber = Box(1,2,3)
    print(f"The gas of the mass of the combustion chamber is: {combustion_chamber.mass:.2f} kg")


    #------- Make orifice plate ------
    plate = Plate(
        width=1000,
        height=600,
        hole_diameter=50,
        number_of_holes=75
    )

    save_plate_png(plate, "plate_design.png")

    print(plate)
    print("PNG saved as plate_design.png")



    #dummy heat source
    Q = 10000 #W


    #Maximum number of iterations
    ite = 100
    # Initialize the while counter
    i = 0
    # set the time step
    dt = 1 #s
    #simulation loop starts here
    while i < ite:
        i += 1
        combustion_chamber.heat_addtion(Q,dt)


    print(combustion_chamber.temperature)
    print(combustion_chamber.pressure)

    # --------------- flow rate test----

    flow_test = combustion_chamber.massflow(101325,plate)

    print(f" The flow in through the orifice is: {flow_test}")


main()
