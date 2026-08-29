class Box:
    def __init__(self,height,width,depth):
        self.height = height
        self.width = width
        self.depth = depth

        self.temperature = 273              #°K
        self.pressure = 101325              #Pa
        self.molarmass = 28.97 / 1000       #mol / kg

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
