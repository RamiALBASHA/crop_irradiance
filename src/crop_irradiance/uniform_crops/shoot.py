from crop_irradiance.uniform_crops.formalisms import lumped_leaves, sunlit_shaded_leaves
from crop_irradiance.uniform_crops.inputs import LumpedInputs, SunlitShadedInputs
from crop_irradiance.uniform_crops.params import LumpedParams, SunlitShadedParams


class LeafLayer:
    def __init__(
        self, index: int, upper_cumulative_leaf_area_index: float, thickness: float
    ):
        self.index = index
        self.upper_cumulative_leaf_area_index = upper_cumulative_leaf_area_index
        self.thickness = thickness
        self.absorbed_irradiance = {}

    def calc_absorbed_irradiance(
        self,
        inputs: LumpedInputs or SunlitShadedInputs,
        params: LumpedParams or SunlitShadedParams,
    ):
        pass


class LumpedLeafLayer(LeafLayer):
    def __init__(
        self, index: int, upper_cumulative_leaf_area_index: float, thickness: float
    ):
        super().__init__(index, upper_cumulative_leaf_area_index, thickness)

    def calc_absorbed_irradiance(self, inputs: LumpedInputs, params: LumpedParams):
        if params.model == "beer":
            self.absorbed_irradiance["lumped"] = lumped_leaves.calc_beer_absorption(
                incident_irradiance=inputs.incident_irradiance,
                extinction_coefficient=params.extinction_coefficient,
                upper_cumulative_leaf_area_index=self.upper_cumulative_leaf_area_index,
                leaf_layer_thickness=self.thickness,
            )
        elif params.model == "de_pury":
            self.absorbed_irradiance["lumped"] = lumped_leaves.calc_de_pury_absorption(
                incident_direct_irradiance=inputs.incident_direct_irradiance,
                incident_diffuse_irradiance=inputs.incident_diffuse_irradiance,
                upper_cumulative_leaf_area_index=self.upper_cumulative_leaf_area_index,
                leaf_layer_thickness=self.thickness,
                direct_extinction_coefficient=params.direct_extinction_coefficient,
                diffuse_extinction_coefficient=params.diffuse_extinction_coefficient,
                canopy_reflectance_to_direct_irradiance=params.canopy_reflectance_to_direct_irradiance,
                canopy_reflectance_to_diffuse_irradiance=params.canopy_reflectance_to_diffuse_irradiance,
            )


class SunlitShadedLeafLayer(LeafLayer):
    def __init__(
        self,
        index: int,
        upper_cumulative_leaf_area_index: float,
        thickness: float,
        params: SunlitShadedParams,
    ):
        super().__init__(index, upper_cumulative_leaf_area_index, thickness)

        self.sunlit_fraction = sunlit_shaded_leaves.calc_sunlit_fraction_per_leaf_layer(
            upper_cumulative_leaf_area_index=self.upper_cumulative_leaf_area_index,
            leaf_layer_thickness=self.thickness,
            direct_black_extinction_coefficient=params.direct_black_extinction_coefficient,
        )

        self.shaded_fraction = 1.0 - self.sunlit_fraction

        self.abs_direct_by_sunlit = None
        self.abs_diffuse_by_sunlit = None
        self.abs_scattered_by_sunlit = None
        self.abs_diffuse_by_shaded = None
        self.abs_scattered_by_shaded = None

    def calc_absorbed_irradiance(
        self, inputs: SunlitShadedInputs, params: SunlitShadedParams
    ):
        self.absorbed_irradiance = sunlit_shaded_leaves.absorbed_irradiance_by_sunlit_and_shaded_leaves_per_leaf_layer(
            incident_direct_irradiance=inputs.incident_direct_irradiance,
            incident_diffuse_irradiance=inputs.incident_diffuse_irradiance,
            upper_cumulative_leaf_area_index=self.upper_cumulative_leaf_area_index,
            leaf_layer_thickness=self.thickness,
            leaf_scattering_coefficient=params.leaf_scattering_coefficient,
            canopy_reflectance_to_direct_irradiance=params.canopy_reflectance_to_direct_irradiance,
            canopy_reflectance_to_diffuse_irradiance=params.canopy_reflectance_to_diffuse_irradiance,
            direct_extinction_coefficient=params.direct_extinction_coefficient,
            direct_black_extinction_coefficient=params.direct_black_extinction_coefficient,
            diffuse_extinction_coefficient=params.diffuse_extinction_coefficient,
        )

        self.abs_direct_by_sunlit = sunlit_shaded_leaves.calc_absorbed_direct_irradiance_by_sunlit_leaf_layer(
            incident_direct_irradiance=inputs.incident_direct_irradiance,
            upper_cumulative_leaf_area_index=self.upper_cumulative_leaf_area_index,
            leaf_layer_thickness=self.thickness,
            leaf_scattering_coefficient=params.leaf_scattering_coefficient,
            direct_black_extinction_coefficient=params.direct_black_extinction_coefficient,
        )

        self.abs_diffuse_by_sunlit = sunlit_shaded_leaves.calc_absorbed_diffuse_irradiance_by_sunlit_leaf_layer(
            incident_diffuse_irradiance=inputs.incident_diffuse_irradiance,
            upper_cumulative_leaf_area_index=self.upper_cumulative_leaf_area_index,
            leaf_layer_thickness=self.thickness,
            canopy_reflectance_to_diffuse_irradiance=params.canopy_reflectance_to_diffuse_irradiance,
            direct_black_extinction_coefficient=params.direct_black_extinction_coefficient,
            diffuse_extinction_coefficient=params.diffuse_extinction_coefficient,
        )

        self.abs_scattered_by_sunlit = sunlit_shaded_leaves.calc_absorbed_scattered_irradiance_by_sunlit_leaf_layer(
            incident_direct_irradiance=inputs.incident_direct_irradiance,
            upper_cumulative_leaf_area_index=self.upper_cumulative_leaf_area_index,
            leaf_layer_thickness=self.thickness,
            direct_extinction_coefficient=params.direct_extinction_coefficient,
            direct_black_extinction_coefficient=params.direct_black_extinction_coefficient,
            canopy_reflectance_to_direct_irradiance=params.canopy_reflectance_to_direct_irradiance,
            leaf_scattering_coefficient=params.leaf_scattering_coefficient,
        )

        self.abs_diffuse_by_shaded = sunlit_shaded_leaves.calc_absorbed_diffuse_irradiance_by_shaded_leaf_layer(
            incident_diffuse_irradiance=inputs.incident_diffuse_irradiance,
            upper_cumulative_leaf_area_index=self.upper_cumulative_leaf_area_index,
            leaf_layer_thickness=self.thickness,
            canopy_reflectance_to_diffuse_irradiance=params.canopy_reflectance_to_diffuse_irradiance,
            direct_black_extinction_coefficient=params.direct_black_extinction_coefficient,
            diffuse_extinction_coefficient=params.diffuse_extinction_coefficient,
        )

        self.abs_scattered_by_shaded = sunlit_shaded_leaves.calc_absorbed_scattered_irradiance_by_shaded_leaf_layer(
            incident_direct_irradiance=inputs.incident_direct_irradiance,
            upper_cumulative_leaf_area_index=self.upper_cumulative_leaf_area_index,
            leaf_layer_thickness=self.thickness,
            direct_extinction_coefficient=params.direct_extinction_coefficient,
            direct_black_extinction_coefficient=params.direct_black_extinction_coefficient,
            canopy_reflectance_to_direct_irradiance=params.canopy_reflectance_to_direct_irradiance,
            leaf_scattering_coefficient=params.leaf_scattering_coefficient,
        )


class Shoot(dict):
    def __init__(
        self,
        leaves_category: str,
        inputs: LumpedInputs or SunlitShadedInputs,
        params: LumpedParams or SunlitShadedParams,
    ):
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

        super().__init__()

        self.inputs = inputs
        self.params = params
        self._leaf_layer_indexes = list(reversed(sorted(inputs.leaf_layers.keys())))

        self.set_leaf_layers(leaves_category)

    def set_leaf_layers(self, leaves_category: str):
        """Sets leaf layers of the shoot.

        Args:
            leaves_category: one of ('lumped', 'sunlit-shaded')
        """

        upper_cumulative_leaf_area_index = 0.0
        for index in self._leaf_layer_indexes:
            layer_thickness = self.inputs.leaf_layers[index]
            if leaves_category == "lumped":
                self[index] = LumpedLeafLayer(
                    index, upper_cumulative_leaf_area_index, layer_thickness
                )
            else:
                self[index] = SunlitShadedLeafLayer(
                    index,
                    upper_cumulative_leaf_area_index,
                    layer_thickness,
                    self.params,
                )

            upper_cumulative_leaf_area_index += layer_thickness

    def calc_absorbed_irradiance(self):
        """Calculates the absorbed irradiance by shoot's layers."""
        for index in self._leaf_layer_indexes:
            self[index].calc_absorbed_irradiance(self.inputs, self.params)
