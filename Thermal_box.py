import numpy as np


class Box:
    UNIVERSAL_GAS_CONSTANT = 8.314  # J / (mol * K)

    def __init__(self, height: float, width: float, depth: float):
        self.height = height
        self.width = width
        self.depth = depth

        self.temperature = 273.15  # K
        self.pressure = 101325.0  # Pa
        self.molar_mass = 27.7 / 1000.0  # kg / mol

        self.kappa = 1.4
        self.gas_constant = self.UNIVERSAL_GAS_CONSTANT / self.molar_mass  # J / (kg * K)
        self.density = self.pressure / (self.temperature * self.gas_constant)  # kg / m^3

        # Specific heat capacity: J / (kg * K)
        self.cp = (7 / 2) * self.gas_constant * 1.3

        self.volume: float = self.height * self.width * self.depth  # m^3
        self.mass: float = self.volume * self.density  # kg

    def heat_addition(self, heat: float, dt: float) -> None:
        """Add heat (Watts) over time step dt (seconds)."""
        # dT = Q / (m * cp)
        self.temperature += (heat * dt) / (self.mass * self.cp)
        self.update_pressure()
        self.update_density()

    def update_density(self) -> None:
        self.density = self.pressure / (self.temperature * self.gas_constant)

    def update_pressure(self) -> None:
        self.pressure = (self.mass * self.gas_constant * self.temperature) / self.volume

    def mass_change(self, mass_flux: float, dt: float) -> None:
        """Update mass with mass_flux (kg/s) over time step dt (seconds)."""
        self.mass += mass_flux * dt
        self.update_pressure()
        self.update_density()

    def massflow(self, pressure_downstream: float, orifice: object) -> float:
        """Calculate mass flow rate through an orifice (kg/s)."""
        if self.pressure == pressure_downstream:
            return 0.0

        is_outflow = self.pressure > pressure_downstream
        p_high = self.pressure if is_outflow else pressure_downstream
        p_low = pressure_downstream if is_outflow else self.pressure

        k = self.kappa
        T = self.temperature
        R = self.gas_constant
        c_d = 0.5

        area = np.pi * (orifice.hole_diameter / 1000.0) ** 2 / 4.0
        critical_ratio = ((k + 1) / 2) ** (k / (k - 1))  # ~1.893 for k=1.4
        pressure_ratio = p_high / p_low

        if pressure_ratio > critical_ratio:
            # Choked flow
            flow = c_d * area * np.sqrt((k * p_high**2 / (R * T)) * (2 / (k + 1)) ** ((k + 1) / (k - 1)))
        else:
            # Subsonic (unchoked) flow
            pr = p_low / p_high
            factor = (pr ** (2 / k)) - (pr ** ((k + 1) / k))
            flow = c_d * area * p_high * np.sqrt((2 * k / (R * T * (k - 1))) * factor)

        return -flow if is_outflow else flow

    def heat_release(self, q_fuel: float, t_end: float, dt: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Compute cumulative energy release and rate over time."""
        time = np.arange(0, t_end + dt, dt)
        t_0 = 0.1
        d_t = 1.0
        m = 2
        alpha = 5

        energy = np.zeros_like(time)
        active = time >= t_0
        energy[active] = (1 - np.exp(-alpha * ((time[active] - t_0) / d_t) ** (m + 1))) * q_fuel

        heat_flow = np.diff(energy, prepend=energy[0]) / dt
        return time, energy, heat_flow
