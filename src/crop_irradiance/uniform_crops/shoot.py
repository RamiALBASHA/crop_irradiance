from crop_irradiance.uniform_crops.formalisms import lumped_leaves


class ShootParameters:
    def __init__(self, **kwargs):
        for attribute, value in kwargs.items():
            setattr(self, attribute, value)


class OutsideIrradiance:
    def __init__(self, **kwargs):
        for attribute, value in kwargs.items():
            setattr(self, attribute, value)


class LeafLayer:
    def __init__(self,
                 index: int,
                 upper_cumulative_leaf_area_index: float,
                 thickness: float):
        self.index = index
        self.upper_cumulative_leaf_area_index = upper_cumulative_leaf_area_index
        self.thickness = thickness
        self.absorbed_irradiance = None
        self.transmitted_irradiance = None

    def calc_absorbed_irradiance(self,
                                 incident_irradiance: float,
                                 extinction_coefficient: float):
        upper_absorbed_irradiance = lumped_leaves.calc_beer_absorption(
            incident_irradiance, extinction_coefficient, self.upper_cumulative_leaf_area_index)
        lower_absorbed_irradiance = lumped_leaves.calc_beer_absorption(
            incident_irradiance, extinction_coefficient, self.upper_cumulative_leaf_area_index + self.thickness)

        self.absorbed_irradiance = (lower_absorbed_irradiance - upper_absorbed_irradiance)


class Shoot(dict):
    def __init__(self,
                 leaf_layers: dict,
                 params: ShootParameters,
                 outside_irradiance: OutsideIrradiance):

        dict.__init__(self)

        self._leaf_layer_indexes = list(reversed(sorted(leaf_layers.keys())))
        self.params = params
        self.outside_irradiance = outside_irradiance

        self.set_leaf_layers(leaf_layers)
        self.calc_leaf_layer_absorbed_irradiance(params)

    def __getitem__(self, key):
        val = dict.__getitem__(self, key)
        return val

    def __setitem__(self, key, val):
        dict.__setitem__(self, key, val)

    def set_leaf_layers(self, leaf_layers: dict):

        upper_cumulative_leaf_area_index = 0.0
        for index in self._leaf_layer_indexes:
            layer_thickness = leaf_layers[index]
            self[index] = LeafLayer(index,
                                    upper_cumulative_leaf_area_index,
                                    layer_thickness)
            upper_cumulative_leaf_area_index += layer_thickness

    def calc_leaf_layer_absorbed_irradiance(self,
                                            params: ShootParameters):
        for index in self._leaf_layer_indexes:
            self[index].calc_absorbed_irradiance(self.outside_irradiance.incident_irradiance,
                                                 params.extinction_coefficient)
