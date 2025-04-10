from crop_irradiance.uniform_crops.formalisms import config, sunlit_shaded_leaves
from crop_irradiance.uniform_crops.inputs import LumpedInputs, SunlitShadedInputs


class LumpedParams:
    def __init__(self, model: str, **kwargs):

        self.model = model
        if "clumping_factor" in kwargs:
            self.clumping_factor = kwargs["clumping_factor"]
        else:
            self.clumping_factor = 1

        if self.model == "beer":
            self.extinction_coefficient = kwargs["extinction_coefficient"]

        elif self.model == "de_pury":
            self.canopy_reflectance_to_diffuse_irradiance = kwargs[
                "canopy_reflectance_to_diffuse_irradiance"
            ]
            self.sky_sectors_number = kwargs["sky_sectors_number"]
            self.sky_type = kwargs["sky_type"]
            if "leaf_angle_distribution_factor" in kwargs:
                self.leaf_angle_distribution_factor = kwargs[
                    "leaf_angle_distribution_factor"
                ]
            else:
                self.leaf_angle_distribution_factor = config.SPHERICAL_ANGLES_FACTOR

            self.leaf_scattering_coefficient = (
                sunlit_shaded_leaves.calc_leaf_scattering_coefficient(
                    leaf_reflectance=kwargs["leaf_reflectance"],
                    leaf_transmittance=kwargs["leaf_transmittance"],
                )
            )

            self.direct_black_extinction_coefficient = None
            self.direct_extinction_coefficient = None
            self.diffuse_extinction_coefficient = None
            self.canopy_reflectance_to_direct_irradiance = None

    def update(self, inputs: LumpedInputs):
        self.direct_black_extinction_coefficient = (
            sunlit_shaded_leaves.calc_direct_black_extinction_coefficient(
                solar_inclination=inputs.solar_inclination,
                leaf_angle_distribution_factor=self.leaf_angle_distribution_factor,
                clumping_factor=self.clumping_factor,
            )
        )

        self.direct_extinction_coefficient = (
            sunlit_shaded_leaves.calc_direct_extinction_coefficient(
                solar_inclination=inputs.solar_inclination,
                leaf_scattering_coefficient=self.leaf_scattering_coefficient,
                leaf_angle_distribution_factor=self.leaf_angle_distribution_factor,
                clumping_factor=self.clumping_factor,
            )
        )

        self.diffuse_extinction_coefficient = (
            sunlit_shaded_leaves.calc_diffuse_extinction_coefficient(
                leaf_area_index=sum(inputs.leaf_layers.values()),
                leaf_angle_distribution_factor=self.leaf_angle_distribution_factor,
                clumping_factor=self.clumping_factor,
                leaf_scattering_coefficient=self.leaf_scattering_coefficient,
                sky_sectors_number=self.sky_sectors_number,
                sky_type=self.sky_type,
            )[0]
        )

        self.canopy_reflectance_to_direct_irradiance = sunlit_shaded_leaves.calc_canopy_reflectance_to_direct_irradiance(
            direct_black_extinction_coefficient=self.direct_black_extinction_coefficient,
            leaf_scattering_coefficient=self.leaf_scattering_coefficient,
        )


class SunlitShadedParams:
    def __init__(
        self,
        leaf_reflectance: float,
        leaf_transmittance: float,
        sky_sectors_number: int,
        sky_type: str,
        canopy_reflectance_to_diffuse_irradiance: float,
        leaf_angle_distribution_factor: float = config.SPHERICAL_ANGLES_FACTOR,
        clumping_factor: float = 1,
    ):
        self.leaf_angle_distribution_factor = leaf_angle_distribution_factor
        self.sky_sectors_number = sky_sectors_number
        self.sky_type = sky_type
        self.canopy_reflectance_to_diffuse_irradiance = (
            canopy_reflectance_to_diffuse_irradiance
        )
        self.clumping_factor = clumping_factor

        self.direct_black_extinction_coefficient = None
        self.direct_extinction_coefficient = None
        self.diffuse_extinction_coefficient = None
        self.canopy_reflectance_to_direct_irradiance = None

        self.leaf_scattering_coefficient = (
            sunlit_shaded_leaves.calc_leaf_scattering_coefficient(
                leaf_reflectance, leaf_transmittance
            )
        )

    def update(self, inputs: SunlitShadedInputs):
        self.direct_black_extinction_coefficient = (
            sunlit_shaded_leaves.calc_direct_black_extinction_coefficient(
                solar_inclination=inputs.solar_inclination,
                leaf_angle_distribution_factor=self.leaf_angle_distribution_factor,
                clumping_factor=self.clumping_factor,
            )
        )

        self.direct_extinction_coefficient = (
            sunlit_shaded_leaves.calc_direct_extinction_coefficient(
                solar_inclination=inputs.solar_inclination,
                leaf_scattering_coefficient=self.leaf_scattering_coefficient,
                leaf_angle_distribution_factor=self.leaf_angle_distribution_factor,
                clumping_factor=self.clumping_factor,
            )
        )

        self.diffuse_extinction_coefficient = (
            sunlit_shaded_leaves.calc_diffuse_extinction_coefficient(
                leaf_area_index=sum(inputs.leaf_layers.values()),
                leaf_angle_distribution_factor=self.leaf_angle_distribution_factor,
                clumping_factor=self.clumping_factor,
                leaf_scattering_coefficient=self.leaf_scattering_coefficient,
                sky_sectors_number=self.sky_sectors_number,
                sky_type=self.sky_type,
            )[0]
        )

        self.canopy_reflectance_to_direct_irradiance = sunlit_shaded_leaves.calc_canopy_reflectance_to_direct_irradiance(
            direct_black_extinction_coefficient=self.direct_black_extinction_coefficient,
            leaf_scattering_coefficient=self.leaf_scattering_coefficient,
        )
