class Box:
    def __init__(self,height,width,depth):
        self.height = height
        self.width = width
        self.depth = depth

        self.temperature = 273
        self.pressure = 101325
        self.gas_constant = 289
        self.density = self.pressure / (self.temperature * self.gas_constant)

        self.volume: float = self.height*self.width*self.depth
        self.mass: float   = self.volume *self.density
