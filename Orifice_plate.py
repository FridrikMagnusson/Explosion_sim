import warnings

# Suppress the NumPy longdouble warning
warnings.filterwarnings(
    "ignore",
    message=r"Signature .* for <class 'numpy\.longdouble'> does not match any known type.*",
    category=UserWarning,
)


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle

class Plate:
    def __init__(self, width: float, height: float,hole_diameter: float,number_of_holes: int):
        self.width = width
        self.height = height
        self.number_of_holes = number_of_holes
        self.rows = int(np.round(np.sqrt(number_of_holes*self.height/self.width)))
        self.cols = int(np.round(number_of_holes/self.rows))
        self.hole_diameter = hole_diameter

        print(f"There should be rows: {self.rows} and columns: {self.cols}")

        self.holes = self._create_holes()

    def _create_holes(self):
        holes = []

        # Vertical spacing for a hexagonal lattice
        row_spacing = self.height / (self.rows+1)
        col_spacing = self.width / (self.cols+1)

        n_holes = 0

        for row in range(self.rows):
            y = (1+row) * row_spacing
            # Every second row is shifted by half the spacing
            offset = 0 if row % 2 == 0 else col_spacing / 2

            for col in range(self.cols):
                x = (1+col) * col_spacing + offset

                if n_holes < self.number_of_holes:
                    holes.append({
                        "x": x,
                        "y": y,
                        "diameter": self.hole_diameter
                        })

                    n_holes += 1

        return holes

    def __repr__(self):
        return (
            f"Plate({self.width} x {self.height}, "
            f"{len(self.holes)} holes, "
            f"hole diameter={self.hole_diameter})"
        )







def save_plate_png(plate, filename="plate_design.png"):
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plate outline
    plate_rect = Rectangle(
        (0, 0),
        plate.width,
        plate.height,
        facecolor="lightgray",
        edgecolor="black",
        linewidth=2
    )
    ax.add_patch(plate_rect)

    # Draw holes
    radius = plate.hole_diameter / 2

    for hole in plate.holes:
        circle = Circle(
            (hole["x"], hole["y"]),
            radius,
            facecolor="white",
            edgecolor="black",
            linewidth=1
        )
        ax.add_patch(circle)

    # Keep correct proportions
    ax.set_aspect("equal")

    # Plate dimensions
    ax.set_xlim(0, plate.width)
    ax.set_ylim(0, plate.height)

    ax.set_xlabel("Width")
    ax.set_ylabel("Height")
    ax.set_title(
        f"Plate Design — {len(plate.holes)} holes "
        f"(Ø {plate.hole_diameter})"
    )

    # Grid
    ax.grid(True, linestyle="--", alpha=0.3)

    # Save PNG
    plt.savefig(
        filename,
        dpi=300,
        bbox_inches="tight",
        facecolor="white"
    )

    plt.close(fig)
