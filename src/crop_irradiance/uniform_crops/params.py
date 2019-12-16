from crop_irradiance.uniform_crops.formalisms import sunlit_shaded_leaves
from crop_irradiance.uniform_crops.inputs import SunlitShadedInputs


class LumpedParams:
    def __init__(self, extinction_coefficient: float):
        self.extinction_coefficient = extinction_coefficient


class SunlitShadedParams:
    def __init__(self,
                 leaf_reflectance: float,
                 leaf_transmittance: float,
                 leaves_to_sun_average_projection: float,
                 sky_sectors_number: int,
                 sky_type: str,
                 canopy_reflectance_to_diffuse_irradiance: float):

        self.leaves_to_sun_average_projection = leaves_to_sun_average_projection
        self.sky_sectors_number = sky_sectors_number
        self.sky_type = sky_type
        self.canopy_reflectance_to_diffuse_irradiance = canopy_reflectance_to_diffuse_irradiance

        self.direct_black_extinction_coefficient = None
        self.direct_extinction_coefficient = None
        self.diffuse_extinction_coefficient = None
        self.canopy_reflectance_to_direct_irradiance = None

        self.leaf_scattering_coefficient = sunlit_shaded_leaves.calc_leaf_scattering_coefficient(
            leaf_reflectance, leaf_transmittance)

    def update(self,
               inputs: SunlitShadedInputs):

        self.direct_black_extinction_coefficient = \
            sunlit_shaded_leaves.calc_direct_black_extinction_coefficient(
                solar_inclination=inputs.solar_inclination,
                leaves_to_sun_average_projection=self.leaves_to_sun_average_projection)

        self.direct_extinction_coefficient = \
            sunlit_shaded_leaves.calc_direct_extinction_coefficient(
                solar_inclination=inputs.solar_inclination,
                leaf_scattering_coefficient=self.leaf_scattering_coefficient,
                leaves_to_sun_average_projection=self.leaves_to_sun_average_projection)

        self.diffuse_extinction_coefficient = \
            sunlit_shaded_leaves.calc_diffuse_extinction_coefficient(
                leaf_area_index=sum(inputs.leaf_layers.values()),
                leaf_scattering_coefficient=self.leaf_scattering_coefficient,
                sky_sectors_number=self.sky_sectors_number,
                sky_type=self.sky_type)[0]

        self.canopy_reflectance_to_direct_irradiance = \
            sunlit_shaded_leaves.calc_canopy_reflectance_to_direct_irradiance(
                direct_black_extinction_coefficient=self.direct_black_extinction_coefficient,
                leaf_scattering_coefficient=self.leaf_scattering_coefficient)
