from crop_irradiance.uniform_crops.formalisms import lumped_leaves, sunlit_shaded_leaves
from crop_irradiance.uniform_crops.inputs import LumpedInputs, SunlitShadedInputs
from crop_irradiance.uniform_crops.params import LumpedParams, SunlitShadedParams


class LeafLayer:
    def __init__(self,
                 index: int,
                 upper_cumulative_leaf_area_index: float,
                 thickness: float):
        self.index = index
        self.upper_cumulative_leaf_area_index = upper_cumulative_leaf_area_index
        self.thickness = thickness
        self.absorbed_irradiance = {}

    def calc_absorbed_irradiance(self,
                                 inputs: LumpedInputs or SunlitShadedInputs,
                                 params: LumpedParams or SunlitShadedParams):
        pass


class LumpedLeafLayer(LeafLayer):
    def __init__(self,
                 index: int,
                 upper_cumulative_leaf_area_index: float,
                 thickness: float):
        LeafLayer.__init__(self, index, upper_cumulative_leaf_area_index, thickness)

    def calc_absorbed_irradiance(self,
                                 inputs: LumpedInputs,
                                 params: LumpedParams):
        upper_absorbed_irradiance = lumped_leaves.calc_beer_absorption(
            incident_irradiance=inputs.incident_irradiance,
            extinction_coefficient=params.extinction_coefficient,
            leaf_area_index=self.upper_cumulative_leaf_area_index)
        lower_absorbed_irradiance = lumped_leaves.calc_beer_absorption(
            incident_irradiance=inputs.incident_irradiance,
            extinction_coefficient=params.extinction_coefficient,
            leaf_area_index=self.upper_cumulative_leaf_area_index + self.thickness)

        self.absorbed_irradiance['lumped'] = (lower_absorbed_irradiance - upper_absorbed_irradiance)


class SunlitShadedLeafLayer(LeafLayer):
    def __init__(self,
                 index: int,
                 upper_cumulative_leaf_area_index: float,
                 thickness: float,
                 params: SunlitShadedParams):
        LeafLayer.__init__(self, index, upper_cumulative_leaf_area_index, thickness)

        self.sunlit_fraction = None
        self.shaded_fraction = None

        self.set_leaf_fractions(params)

    def set_leaf_fractions(self,
                           params: SunlitShadedParams):
        upper_sunlit_fraction = sunlit_shaded_leaves.calc_sunlit_fraction(
            cumulative_leaf_area_index=self.upper_cumulative_leaf_area_index,
            direct_black_extinction_coefficient=params.direct_black_extinction_coefficient)
        lower_sunlit_fraction = sunlit_shaded_leaves.calc_sunlit_fraction(
            cumulative_leaf_area_index=self.upper_cumulative_leaf_area_index + self.thickness,
            direct_black_extinction_coefficient=params.direct_black_extinction_coefficient)

        self.sunlit_fraction = (upper_sunlit_fraction - lower_sunlit_fraction) / (
                params.direct_black_extinction_coefficient * self.thickness)

        self.shaded_fraction = 1.0 - self.sunlit_fraction

    def calc_absorbed_irradiance(self,
                                 inputs: SunlitShadedInputs,
                                 params: SunlitShadedParams):
        self.absorbed_irradiance = \
            sunlit_shaded_leaves.absorbed_irradiance_by_sunlit_and_shaded_leaves_per_leaf_layer(
                incident_direct_irradiance=inputs.incident_direct_irradiance,
                incident_diffuse_irradiance=inputs.incident_diffuse_irradiance,
                upper_cumulative_leaf_area_index=self.upper_cumulative_leaf_area_index,
                leaf_layer_thickness=self.thickness,
                leaf_scattering_coefficient=params.leaf_scattering_coefficient,
                canopy_reflectance_to_direct_irradiance=params.canopy_reflectance_to_direct_irradiance,
                canopy_reflectance_to_diffuse_irradiance=params.canopy_reflectance_to_diffuse_irradiance,
                direct_extinction_coefficient=params.direct_extinction_coefficient,
                direct_black_extinction_coefficient=params.direct_black_extinction_coefficient,
                diffuse_extinction_coefficient=params.diffuse_extinction_coefficient)


class Shoot(dict):
    def __init__(self,
                 leaves_category: str,
                 inputs: LumpedInputs or SunlitShadedInputs,
                 params: LumpedParams or SunlitShadedParams):
        """Creates a class:`Shoot` object having either 'lumped' leaves or 'sunlit-shaded' leaves.

        Args:
            leaves_category: one of ('lumped', 'sunlit-shaded')
            inputs: see class`LumpedInputs` and `SunlitShadedInputs`
            params: see class`LumpedParams` and `SunlitShadedParams`

        Notes:
            The created shoot can implicitly be 'big-leaf' or a 'layered'. If the attribute `leaf_layers` of the
                :Class:`inputs` object has only one layer, then the resulting shoot is a 'big-leaf', otherwise if the
                dictionary has more than one key, then the shoot is 'layered'.
            Leaf layers indexes in `leaf_layers` must be ordered so that the youngest leaf layer has the highest index
                value, and inversely, the oldest leaf layer has the least value. Not respecting this order will
                definitely lead to erroneous calculations.
        """

        dict.__init__(self)

        self.inputs = inputs
        self.params = params
        self._leaf_layer_indexes = list(reversed(sorted(inputs.leaf_layers.keys())))

        self.set_leaf_layers(leaves_category)
        self.calc_absorbed_irradiance()

    def __getitem__(self, key):
        val = dict.__getitem__(self, key)
        return val

    def __setitem__(self, key, val):
        dict.__setitem__(self, key, val)

    def set_leaf_layers(self, leaves_category: str):
        """Sets leaf layers of the shoot.

        Args:
            leaves_category: one of ('lumped', 'sunlit-shaded')
        """

        upper_cumulative_leaf_area_index = 0.0
        for index in self._leaf_layer_indexes:
            layer_thickness = self.inputs.leaf_layers[index]
            if leaves_category == 'lumped':
                self[index] = LumpedLeafLayer(index,
                                              upper_cumulative_leaf_area_index,
                                              layer_thickness)
            else:
                self[index] = SunlitShadedLeafLayer(index,
                                                    upper_cumulative_leaf_area_index,
                                                    layer_thickness,
                                                    self.params)

            upper_cumulative_leaf_area_index += layer_thickness

    def calc_absorbed_irradiance(self):
        """Calculates the absorbed irradiance by shoot's layers.
        """
        for index in self._leaf_layer_indexes:
            self[index].calc_absorbed_irradiance(self.inputs, self.params)
