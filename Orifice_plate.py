import warnings
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Circle, Rectangle
import numpy as np

# Suppress the NumPy longdouble warning if applicable
warnings.filterwarnings(
    "ignore",
    message=r"Signature .* for <class 'numpy\.longdouble'> does not match any known type.*",
    category=UserWarning,
)


class Plate:
    def __init__(
        self,
        width: float,
        height: float,
        hole_diameter: float,
        number_of_holes: int,
    ):
        self.width = width
        self.height = height
        self.hole_diameter = hole_diameter
        self.number_of_holes = number_of_holes

        # Ensure at least 1 row and 1 column to prevent ZeroDivisionError
        self.rows = max(1, int(np.round(np.sqrt(number_of_holes * self.height / self.width))))
        self.cols = max(1, int(np.ceil(number_of_holes / self.rows)))

        self.holes = self._create_holes()

    def _create_holes(self) -> np.ndarray:
        """Generate (x, y) center coordinates for each hole."""
        row_spacing = self.height / (self.rows + 1)
        col_spacing = self.width / (self.cols + 1)

        coords = []
        for r in range(self.rows):
            y = (r + 1) * row_spacing
            offset = col_spacing / 4 if (r % 2 == 1) else -col_spacing / 4

            for c in range(self.cols):
                if len(coords) >= self.number_of_holes:
                    break
                x = (c + 1) * col_spacing + offset
                coords.append((x, y))

        return np.array(coords)

    def __repr__(self) -> str:
        return (
            f"Plate(width={self.width}, height={self.height}, "
            f"holes={len(self.holes)}, hole_diameter={self.hole_diameter})"
        )


def save_plate_png(plate: Plate, filename: str = "plate_design.png", dpi: int = 300) -> None:
    """Renders the plate and hole layout to a PNG image file."""
    fig, ax = plt.subplots(figsize=(10, 6))

    # Base plate
    plate_rect = Rectangle(
        (0, 0),
        plate.width,
        plate.height,
        facecolor="lightgray",
        edgecolor="black",
        linewidth=2,
    )
    ax.add_patch(plate_rect)

    # Batch render holes using PatchCollection for performance
    radius = plate.hole_diameter / 2.0
    patches = [Circle((x, y), radius) for x, y in plate.holes]
    collection = PatchCollection(
        patches,
        facecolor="white",
        edgecolor="black",
        linewidth=1,
        match_original=False,
    )
    ax.add_collection(collection)

    # Formatting
    ax.set_aspect("equal")
    ax.set_xlim(0, plate.width)
    ax.set_ylim(0, plate.height)
    ax.set_xlabel("Width")
    ax.set_ylabel("Height")
    ax.set_title(f"Plate Design — {len(plate.holes)} holes (Ø {plate.hole_diameter})")
    ax.grid(True, linestyle="--", alpha=0.3)

    plt.savefig(filename, dpi=dpi, bbox_inches="tight", facecolor="white")
    plt.close(fig)  # Prevents memory accumulation
