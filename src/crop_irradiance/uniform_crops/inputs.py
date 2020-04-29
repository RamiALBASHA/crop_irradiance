class LumpedInputs:
    def __init__(self,
                 model: str,
                 leaf_layers: dict,
                 **kwargs):

        self.leaf_layers = leaf_layers

        if model == 'beer':
            self.incident_irradiance = kwargs['incident_irradiance']
        elif model == 'de_pury':
            self.incident_direct_irradiance = kwargs['incident_direct_irradiance']
            self.incident_diffuse_irradiance = kwargs['incident_diffuse_irradiance']
            self.solar_inclination = kwargs['solar_inclination']


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
