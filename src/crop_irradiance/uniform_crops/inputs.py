class LumpedInputs:
    def __init__(self,
                 leaf_layers: dict,
                 incident_irradiance: float):

        self.leaf_layers = leaf_layers
        self.incident_irradiance = incident_irradiance


class SunlitShadedInputs:
    def __init__(self,
                 leaf_layers: dict,
                 incident_direct_irradiance: float,
                 incident_diffuse_irradiance: float,
                 solar_inclination: float):

        self.leaf_layers = leaf_layers
        self.incident_direct_irradiance = incident_direct_irradiance
        self.incident_diffuse_irradiance = incident_diffuse_irradiance
        self.solar_inclination = solar_inclination
