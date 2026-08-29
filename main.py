
from Thermal_box import Box


def main():
    print("hallo World")
    combustion_chamber = Box(1,2,3)
    print(f"The gas of the mass of the combustion chamber is: {combustion_chamber.mass:.2f} kg")

main()
