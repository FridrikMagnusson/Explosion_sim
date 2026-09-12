from pathlib import Path
import matplotlib.pyplot as plt

from Orifice_plate import Plate, save_plate_png
from Thermal_box import Box

ATM_PRESSURE = 101325  # Pa
OUTPUT_DIR = Path("output")


def save_line_plot(x, y, x_label, y_label, title, filename):
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, linewidth=2)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    if title:
        plt.title(title)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    # Save directly into the output directory
    plt.savefig(OUTPUT_DIR / filename, dpi=150, bbox_inches="tight")
    plt.close()


def main():
    # Ensure the output directory exists
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Computational domains
    combustion_chamber = Box(1, 1, 1)
    filter_chamber = Box(1, 1, 1)

    # Orifice plates saved into the folder
    plate = Plate(width=1000, height=1000, hole_diameter=50, number_of_holes=72)
    save_plate_png(plate, str(OUTPUT_DIR / "plate_design.png"))

    blast_device = Plate(width=1000, height=1000, hole_diameter=300, number_of_holes=1)
    save_plate_png(blast_device, str(OUTPUT_DIR / "blast_device.png"))

    # Simulation parameters
    q_total = 3.42e6
    iterations = 10000
    dt = 0.0001
    t_end = iterations * dt

    t, _, de_dt = combustion_chamber.heat_release(q_total, t_end, dt)

    pressures = [combustion_chamber.pressure]
    masses = [combustion_chamber.mass]
    flows = [0]

    for i in range(iterations):
        combustion_chamber.heat_addition(de_dt[i], dt)

        unit_flow = combustion_chamber.massflow(filter_chamber.pressure, plate)
        total_plate_flow = plate.number_of_holes * unit_flow


        combustion_chamber.mass_change(total_plate_flow, dt)
        filter_chamber.mass_change(-total_plate_flow, dt)

        blast_flow = filter_chamber.massflow(ATM_PRESSURE, blast_device)
        filter_chamber.mass_change(blast_flow, dt)

        pressures.append(combustion_chamber.pressure)
        masses.append(combustion_chamber.mass)
        flows.append(total_plate_flow)

    # Result plots saved into the folder
    save_line_plot(t, pressures[:len(t)], "Time [s]", "Pressure [Pa]", "Combustion Chamber Pressure", "press_flow.png")
    save_line_plot(t, masses[:len(t)], "Time [s]", "Mass [kg]", "Combustion Chamber Mass", "mass.png")
    save_line_plot(t, flows[:len(t)], "Time [s]", "kg/s [Pa]", "Combustion Chamber outflow", "flow.png")


if __name__ == "__main__":
    main()
