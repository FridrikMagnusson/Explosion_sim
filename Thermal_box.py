from numpy import pi
import numpy as np

class Box:
    def __init__(self,height,width,depth):
        self.height = height
        self.width = width
        self.depth = depth

        self.temperature = 273              #°K
        self.pressure = 101325              #Pa
        self.molarmass = 28.97 / 1000       #mol / kg

        self.kappa = 1.4

        self.universal_gas_constant = 8.314
        self.gas_constant = 8.314 / self.molarmass  #J / kg.K
        self.density = self.pressure / (self.temperature * self.gas_constant) #Kg/m3

        self.cp = 7/2 * self.universal_gas_constant / self.molarmass # J / kg.K

        self.volume: float = self.height*self.width*self.depth # m3
        self.mass: float   = self.volume *self.density          # kg

    def heat_addtion(self,heat,dt):

        self.temperature += heat*dt/self.cp

        self.update_pressure()
        self.update_density()


    def update_density(self):
        self.density = self.pressure / (self.temperature * self.gas_constant) #Kg/m3
        #print("updated density")

    def update_pressure(self):
        self.pressure = self.mass * self.gas_constant * self.temperature / self.volume
        #print("updated pressure")

    def mass_change(self, mass_flux,dt):
        #Input mass_flux kg/s
        self.mass += mass_flux*dt
        self.update_pressure()
        self.update_density()



    def massflow(self,pressure_downstream: float,orifice: object)-> float:

        #TODO - Validate towards litterature.

        pressure_upstream = self.pressure
        p = self.pressure
        p2 = pressure_downstream

        k = self.kappa
        T = self.temperature
        R = self.gas_constant

        c_D = 0.5

        A_V = orifice.hole_diameter/1000**2/4*pi #[m2]

        if pressure_upstream > pressure_downstream:
            print("outflow")
            if pressure_upstream/pressure_downstream > 1.893: #<--choked flow:

                print("choked_flow")
                m_dot = -c_D * A_V*np.sqrt((k * p ** 2 / R / T * (2 / (k + 1)) ** ((k + 1) / (k - 1)))) #[kg/s]

            else:
                print("unchoked_flow")
                m_dot = -c_D*A_V*np.sqrt(2)*np.sqrt((p ** 2 / R / T * k / (k - 1) * ((p2 / p) ** (2 / k) - (p2 / p) ** ((k + 1) / k))))

        elif pressure_upstream < pressure_downstream:
            print("inflow")
            if pressure_downstream/pressure_upstream > 1.893: #<--choked flow:
                print("choked_flow")
                m_dot = c_D * A_V*np.sqrt((k * p2 ** 2 / R / T * (2 / (k + 1)) ** ((k + 1) / (k - 1)))) #[kg/s]
            else:
                print("unchoked_flow")
                m_dot = c_D*A_V*np.sqrt(2)*np.sqrt((p2 ** 2 / R / T * k / (k - 1) * ((p / p2) ** (2 / k) - (p / p2) ** ((k + 1) / k)))) #[kg/s]

        else:
            m_dot = 0

        return m_dot




    def heat_release(self, Q_fuel: float,t_end:float, dt: float) -> list:


        time = np.arange(0, t_end + dt, dt)
        t_0 = 0.1
        d_t = 1
        m = 2
        alpha = 5

        heat = (1 - np.exp(-alpha * ((time - t_0) / d_t) ** (m + 1))) * Q_fuel

        return [time, heat]
