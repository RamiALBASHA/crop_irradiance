from math import sin, sqrt, pi, exp, log


def calc_leaf_scattering_coefficient(leaf_reflectance: float, leaf_transmittance: float) -> float:
    """Calculates leaf scattering coefficient.

    Args:
        leaf_reflectance: [-] leaf reflectance coefficient for a given irradiance band
        leaf_transmittance: [-] leaf transmittance coefficient for a given irradiance band

    Returns:
        [-] leaf scattering coefficient

    References:
        Goudriaan J. (1977).
            Crop Micrometeorology: A Simulation Study.
            Simulation monographs, Pudoc, Wageningen, 257 pp.
    """
    return leaf_reflectance + leaf_transmittance


def calc_direct_black_extinction_coefficient(solar_inclination: float,
                                             leaves_to_sun_average_projection: float = 0.5) -> float:
    """Calculates the extinction coefficient of direct (beam) irradiance through a canopy of black leaves.

    Args:
        solar_inclination: [rad] angle of solar inclination
        leaves_to_sun_average_projection: [-] average projection of canopy leaves in the direction of the solar beam

    Returns:
        [m2ground m-2leaf] the extinction coefficient of direct (beam) irradiance through a canopy of black leaves

    References:
        Goudriaan J. (1977).
            Crop Micrometeorology: A Simulation Study.
            Simulation monographs, Pudoc, Wageningen, 257 pp.
    """
    return leaves_to_sun_average_projection / sin(max(1.e-6, solar_inclination))


def calc_direct_extinction_coefficient(solar_inclination: float, leaf_scattering_coefficient: float,
                                       leaves_to_sun_average_projection: float = 0.5) -> float:
    """Calculates the extinction coefficient of direct (beam) irradiance through a canopy.

    Args:
        solar_inclination: [rad] angle of solar inclination
        leaf_scattering_coefficient: [-] leaf scattering coefficient
        leaves_to_sun_average_projection: [-] average projection of canopy leaves in the direction of the solar beam

    Returns:
        [m2ground m-2leaf] the extinction coefficient of direct (beam) irradiance through the canopy

    References:
        Goudriaan J. (1977).
            Crop Micrometeorology: A Simulation Study.
            Simulation monographs, Pudoc, Wageningen, 257 pp.
    """

    direct_black_extinction_coefficient = calc_direct_black_extinction_coefficient(solar_inclination,
                                                                                   leaves_to_sun_average_projection)

    return direct_black_extinction_coefficient * sqrt(1 - leaf_scattering_coefficient)


def calc_sky_sectors_weight(sky_sectors_number: int, sky_type: str) -> [tuple]:
    """Calculates the contributions from sky sectors (rings) to diffuse irradiance.

    Args:
        sky_sectors_number: [-] number of sky sectors to be used
        sky_type: one of 'soc' or 'uoc' (Sky OverCast and Uniform OverCast, respectively)

    Returns:
        [-] the contributions from sky sectors (rings) to diffuse irradiance
    """
    sky_weights = []
    if sky_type == 'uoc':
        assert sky_sectors_number == 3, ''
        sky_weights = [0.25, 0.5, 0.25]
    elif sky_type == 'soc':
        sky_weights = []
        angle_increment = (pi / 2.0) / sky_sectors_number / 2.0  # half increment in sky ring declination angle
        for i in range(sky_sectors_number):
            lower_angle = i * 2.0 * angle_increment
            upper_angle = (i + 1) * 2.0 * angle_increment
            # Weight factor for each sky ring, the value 7.0/6.0 results from integrating
            # weights over the sky hemisphere, thus used for normalization.
            weight = (sin(upper_angle) ** 2 * (0.5 + 2.0 / 3.0 * sin(upper_angle)) - sin(lower_angle) ** 2 * (
                    0.5 + 2.0 / 3.0 * (sin(lower_angle)))) / (7.0 / 6.0)
            sky_weights.append(weight)

    return sky_weights


def calc_diffuse_extinction_coefficient(leaf_area_index: float,
                                        leaf_scattering_coefficient: float,
                                        sky_sectors_number: int = 3,
                                        sky_type: str = 'soc') -> (float, float):
    """Calculates the diffuse extinction coefficients for canopies with non-black and black leaves.

    Args:
        leaf_area_index: [m2leaf m-2ground] leaf area index of the whole canopy
        leaf_scattering_coefficient: [-] leaf scattering coefficient
        sky_sectors_number: [-] number of sky sectors to be used
        sky_type: one of 'soc' or 'uoc' (Sky OverCast and Uniform OverCast, respectively)

    Returns:
        [m2ground m-2leaf] the extinction coefficient of diffuse irradiance through a canopy of non-black leaves
        [m2ground m-2leaf] the extinction coefficient of diffuse irradiance through a canopy of black leaves

    References:
        Goudriaan J. (1988)
            The bare bones of leaf-angle distribution in radiation models for canopy photosynthesis and energy exchange.
            Agricultural and Forest Meteorology 43, 155 - 169.
    """
    leaf_area_index = max(1.e-6, leaf_area_index)
    sky_weights = calc_sky_sectors_weight(sky_sectors_number, sky_type)

    angle_increment = (pi / 2.0) / sky_sectors_number / 2.0  # half increment in sky ring declination angle

    diffuse_extinction_coefficient = 0.0
    diffuse_black_extinction_coefficient = 0.0

    for i in range(sky_sectors_number):
        sector_angle = angle_increment * (1.0 + 2.0 * i)
        diffuse_extinction_coefficient += sky_weights[i] * exp(
            -(0.5 / sin(sector_angle)) * sqrt(1.0 - leaf_scattering_coefficient) * leaf_area_index)

        diffuse_black_extinction_coefficient += sky_weights[i] * exp(-(0.5 / sin(sector_angle)) * leaf_area_index)

    diffuse_extinction_coefficient = -1.0 / leaf_area_index * log(diffuse_extinction_coefficient)
    diffuse_black_extinction_coefficient = -1.0 / leaf_area_index * log(diffuse_black_extinction_coefficient)

    return diffuse_extinction_coefficient, diffuse_black_extinction_coefficient


def calc_canopy_reflectance_to_direct_irradiance(direct_black_extinction_coefficient: float,
                                                 leaf_scattering_coefficient: float) -> float:
    """Calculates canopy reflectance to direct (beam) irradiance.

    Args:
        direct_black_extinction_coefficient: [m2ground m-2leaf] the extinction coefficient of direct (beam) irradiance
            through a canopy of black leaves
        leaf_scattering_coefficient: [-] leaf scattering coefficient

    Returns:
        [-] canopy reflectance to direct (beam) irradiance
    """
    reflectance_of_horizontal_leaves = (1.0 - sqrt(1 - leaf_scattering_coefficient)) / (
            1.0 + sqrt(1 - leaf_scattering_coefficient))
    return 1.0 - exp(-(2.0 * reflectance_of_horizontal_leaves * direct_black_extinction_coefficient) / (
            1.0 + direct_black_extinction_coefficient))


def get_canopy_reflectance_to_diffuse_irradiance(irradiance_band: str) -> float:
    """Returns default canopy reflectance to diffuse irradiance for a given irradiance band.

    Args:
        irradiance_band: irradiance band, one of ("par", "nir")

    Returns:
        [-] default canopy reflectance to diffuse irradiance for a given irradiance band
    """
    if irradiance_band == 'par':
        return 0.057
    elif irradiance_band == 'nir':
        return 0.389
    else:
        raise ValueError('"irradiance_band" must be one of ("par", "nir")')


def calc_sunlit_fraction(cumulative_leaf_area_index: float, direct_black_extinction_coefficient: float) -> float:
    """Calculates the fraction of sunlit leaves at a given depth inside the canopy.

    Args:
        cumulative_leaf_area_index: [m2leaf m-2ground] cumulative downwards leaf area index
        direct_black_extinction_coefficient: [m2ground m-2leaf] the extinction coefficient of direct (beam)
            irradiance for black leaves

    Returns:
        [-] fraction of sunlit leaves at a given depth inside the canopy
    """
    return exp(-direct_black_extinction_coefficient * cumulative_leaf_area_index)


def calc_shaded_fraction(cumulative_leaf_area_index: float, direct_black_extinction_coefficient: float) -> float:
    """Calculates the fraction of shaded leaves at a given depth inside the canopy.

    Args:
        cumulative_leaf_area_index: [m2leaf m-2ground] cumulative downwards leaf area index
        direct_black_extinction_coefficient: [m2ground m-2leaf] the extinction coefficient of direct (beam)
            irradiance for black leaves

    Returns:
        [-] fraction of shaded leaves at a given depth inside the canopy
    """
    return 1 - calc_shaded_fraction(cumulative_leaf_area_index, direct_black_extinction_coefficient)


def calc_absorbed_direct_irradiance(incident_direct_irradiance: float,
                                    leaf_scattering_coefficient: float,
                                    direct_black_extinction_coefficient: float) -> float:
    """Calculates the absorbed direct (beam) irradiance per unit leaf area (depth-independent).

    Args:
        incident_direct_irradiance: [W m-2ground] incident direct (beam) irradiance at the top of the canopy
        leaf_scattering_coefficient: [-] leaf scattering coefficient
        direct_black_extinction_coefficient: [m2ground m-2leaf] the extinction coefficient of direct (beam)
            irradiance for black leaves
    Returns:
        [W m-2leaf] the absorbed direct (beam) irradiance per unit leaf area (depth-independent)
    """
    return incident_direct_irradiance * (1.0 - leaf_scattering_coefficient) * direct_black_extinction_coefficient


def calc_absorbed_diffuse_irradiance_at_given_depth(incident_diffuse_irradiance: float,
                                                    cumulative_leaf_area_index: float,
                                                    canopy_reflectance_to_diffuse_irradiance: float,
                                                    diffuse_extinction_coefficient: float) -> float:
    """Calculates the absorbed diffuse irradiance per unit leaf area at a given depth inside the canopy.

    Args:
        incident_diffuse_irradiance: [W m-2ground] incident diffuse irradiance at the top of the canopy
        cumulative_leaf_area_index: [m2leaf m-2ground] cumulative downwards leaf area index
        canopy_reflectance_to_diffuse_irradiance: [-] canopy reflectance to diffuse irradiance for the given irradiance
            band
        diffuse_extinction_coefficient: [m2ground m-2leaf] the extinction coefficient of diffuse irradiance

    Returns:
        [W m-2leaf] the absorbed diffuse irradiance per unit leaf area at the given depth inside the canopy
    """
    return incident_diffuse_irradiance * (
            1.0 - canopy_reflectance_to_diffuse_irradiance) * diffuse_extinction_coefficient * exp(
        - diffuse_extinction_coefficient * cumulative_leaf_area_index)


def calc_sunlit_fraction_per_leaf_layer(upper_cumulative_leaf_area_index: float,
                                        leaf_layer_thickness: float,
                                        direct_black_extinction_coefficient: float) -> float:
    """Calculates the fraction of sunlit leaves at a given depth inside the canopy.

    Args:
        upper_cumulative_leaf_area_index: [m2leaf m-2ground] cumulative downwards leaf area index at the top of the
            considered layer
        leaf_layer_thickness: [m2leaf m-2ground] leaf area index of the considered layer
        direct_black_extinction_coefficient: [m2ground m-2leaf] the extinction coefficient of direct (beam)
            irradiance for black leaves

    Returns:
        [-] fraction of sunlit leaves of the considered layer
    """
    upper_fraction = calc_sunlit_fraction(upper_cumulative_leaf_area_index, direct_black_extinction_coefficient)
    lower_fraction = calc_sunlit_fraction(upper_cumulative_leaf_area_index + leaf_layer_thickness,
                                          direct_black_extinction_coefficient)
    return (upper_fraction - lower_fraction) / (direct_black_extinction_coefficient * leaf_layer_thickness)


def calc_absorbed_diffuse_irradiance_per_leaf_layer(incident_diffuse_irradiance: float,
                                                    upper_cumulative_leaf_area_index: float,
                                                    leaf_layer_thickness: float,
                                                    canopy_reflectance_to_diffuse_irradiance: float,
                                                    diffuse_extinction_coefficient: float) -> float:
    """Calculates the absorbed diffuse irradiance by a leaf layer per unit ground area.

    Args:
        incident_diffuse_irradiance: [W m-2ground] incident diffuse irradiance at the top of the canopy
        upper_cumulative_leaf_area_index: [m2leaf m-2ground] cumulative downwards leaf area index at the top of the
            considered layer
        leaf_layer_thickness: [m2leaf m-2ground] leaf area index of the considered layer
        canopy_reflectance_to_diffuse_irradiance: [-] canopy reflectance to diffuse irradiance for the given irradiance
            band
        diffuse_extinction_coefficient: [m2ground m-2leaf] the extinction coefficient of diffuse irradiance

    Returns:
        [W m-2ground] the absorbed diffuse irradiance by a leaf layer per unit ground area
    """
    absorbed_upper = calc_absorbed_diffuse_irradiance_at_given_depth(
        incident_diffuse_irradiance,
        upper_cumulative_leaf_area_index,
        canopy_reflectance_to_diffuse_irradiance,
        diffuse_extinction_coefficient)
    absorbed_lower = calc_absorbed_diffuse_irradiance_at_given_depth(
        incident_diffuse_irradiance,
        upper_cumulative_leaf_area_index + leaf_layer_thickness,
        canopy_reflectance_to_diffuse_irradiance,
        diffuse_extinction_coefficient)

    return (absorbed_upper - absorbed_lower) / (diffuse_extinction_coefficient * leaf_layer_thickness)


def calc_absorbed_scattered_irradiance_per_leaf_layer(incident_direct_irradiance: float,
                                                      upper_cumulative_leaf_area_index: float,
                                                      leaf_layer_thickness: float,
                                                      direct_extinction_coefficient: float,
                                                      direct_black_extinction_coefficient: float,
                                                      canopy_reflectance_to_direct_irradiance: float,
                                                      leaf_scattering_coefficient: float) -> float:
    """Calculates the absorbed scattered irradiance by a leaf layer per unit ground area.

    Args:
        incident_direct_irradiance: [W m-2ground] incident direct (beam) irradiance at the top of the canopy
        upper_cumulative_leaf_area_index: [m2leaf m-2ground] cumulative downwards leaf area index at the top of the
            considered layer
        leaf_layer_thickness: [m2leaf m-2ground] leaf area index of the considered layer
        direct_extinction_coefficient: [m2ground m-2leaf] the extinction coefficient of direct (beam) irradiance
        direct_black_extinction_coefficient: [m2ground m-2leaf] the extinction coefficient of direct (beam)
            irradiance for black leaves
        canopy_reflectance_to_direct_irradiance: [-] canopy reflectance to direct (beam) irradiance
        leaf_scattering_coefficient: [-] leaf scattering coefficient

    Returns:
        [W m-2leaf] the absorbed scattered irradiance per unit leaf area at the given depth inside the canopy
    """
    upper_gain_fraction = (1.0 - canopy_reflectance_to_direct_irradiance) * exp(
        -direct_extinction_coefficient * upper_cumulative_leaf_area_index)
    lower_gain_fraction = (1.0 - canopy_reflectance_to_direct_irradiance) * exp(
        -direct_extinction_coefficient * (upper_cumulative_leaf_area_index + leaf_layer_thickness))

    upper_loss_fraction = (1.0 - leaf_scattering_coefficient) * exp(
        -direct_black_extinction_coefficient * upper_cumulative_leaf_area_index)
    lower_loss_fraction = (1.0 - leaf_scattering_coefficient) * exp(
        -direct_black_extinction_coefficient * (upper_cumulative_leaf_area_index + leaf_layer_thickness))

    return incident_direct_irradiance / leaf_layer_thickness * (
            (upper_gain_fraction - lower_gain_fraction) - (upper_loss_fraction - lower_loss_fraction))


def absorbed_irradiance_by_sunlit_leaves_per_leaf_layer(incident_direct_irradiance: float,
                                                        incident_diffuse_irradiance: float,
                                                        upper_cumulative_leaf_area_index: float,
                                                        leaf_layer_thickness: float,
                                                        leaf_scattering_coefficient: float,
                                                        canopy_reflectance_to_direct_irradiance: float,
                                                        canopy_reflectance_to_diffuse_irradiance: float,
                                                        direct_extinction_coefficient: float,
                                                        direct_black_extinction_coefficient: float,
                                                        diffuse_extinction_coefficient: float):
    """Calculates the absorbed irradiance by sunlit leaves of a leaf layer per unit ground area.

    Args:
        incident_direct_irradiance: [W m-2ground] incident direct (beam) irradiance at the top of the canopy
        incident_diffuse_irradiance: [W m-2ground] incident diffuse irradiance at the top of the canopy
        upper_cumulative_leaf_area_index: [m2leaf m-2ground] cumulative downwards leaf area index at the top of the
            considered layer
        leaf_layer_thickness: [m2leaf m-2ground] leaf area index of the considered layer
        leaf_scattering_coefficient: [-] leaf scattering coefficient
        canopy_reflectance_to_direct_irradiance: [-] canopy reflectance to direct (beam) irradiance
        canopy_reflectance_to_diffuse_irradiance: [-] canopy reflectance to diffuse irradiance
        direct_extinction_coefficient: [m2ground m-2leaf] the extinction coefficient of direct (beam) irradiance
        direct_black_extinction_coefficient: [m2ground m-2leaf] the extinction coefficient of direct (beam)
            irradiance for black leaves
        diffuse_extinction_coefficient: [m2ground m-2leaf] the extinction coefficient of diffuse irradiance

    Returns:
        [W m-2ground] the absorbed irradiance by sunlit leaves of a leaf layer per unit ground area
    """

    absorbed_direct_irradiance = calc_absorbed_direct_irradiance(
        incident_direct_irradiance, leaf_scattering_coefficient, direct_black_extinction_coefficient)

    absorbed_diffuse_irradiance = calc_absorbed_diffuse_irradiance_per_leaf_layer(
        incident_diffuse_irradiance,
        upper_cumulative_leaf_area_index,
        leaf_layer_thickness,
        canopy_reflectance_to_diffuse_irradiance,
        diffuse_extinction_coefficient)

    absorbed_scattered_irradiance = calc_absorbed_scattered_irradiance_per_leaf_layer(
        incident_direct_irradiance,
        upper_cumulative_leaf_area_index,
        leaf_layer_thickness,
        direct_extinction_coefficient,
        direct_black_extinction_coefficient,
        canopy_reflectance_to_direct_irradiance,
        leaf_scattering_coefficient)

    sunlit_area = leaf_layer_thickness * calc_sunlit_fraction_per_leaf_layer(
        upper_cumulative_leaf_area_index, leaf_layer_thickness, direct_black_extinction_coefficient)

    return (absorbed_direct_irradiance + absorbed_diffuse_irradiance + absorbed_scattered_irradiance) * sunlit_area


def absorbed_irradiance_by_shaded_leaves_per_leaf_layer(incident_direct_irradiance: float,
                                                        incident_diffuse_irradiance: float,
                                                        upper_cumulative_leaf_area_index: float,
                                                        leaf_layer_thickness: float,
                                                        leaf_scattering_coefficient: float,
                                                        canopy_reflectance_to_direct_irradiance: float,
                                                        canopy_reflectance_to_diffuse_irradiance: float,
                                                        direct_extinction_coefficient: float,
                                                        direct_black_extinction_coefficient: float,
                                                        diffuse_extinction_coefficient: float) -> float:
    """Calculates the absorbed irradiance by shaded leaves of a leaf layer per unit ground area.

    Args:
        incident_direct_irradiance: [W m-2ground] incident direct (beam) irradiance at the top of the canopy
        incident_diffuse_irradiance: [W m-2ground] incident diffuse irradiance at the top of the canopy
        upper_cumulative_leaf_area_index: [m2leaf m-2ground] cumulative downwards leaf area index at the top of the
            considered layer
        leaf_layer_thickness: [m2leaf m-2ground] leaf area index of the considered layer
        leaf_scattering_coefficient: [-] leaf scattering coefficient
        canopy_reflectance_to_direct_irradiance: [-] canopy reflectance to direct (beam) irradiance
        canopy_reflectance_to_diffuse_irradiance: [-] canopy reflectance to diffuse irradiance
        direct_extinction_coefficient: [m2ground m-2leaf] the extinction coefficient of direct (beam) irradiance
        direct_black_extinction_coefficient: [m2ground m-2leaf] the extinction coefficient of direct (beam)
            irradiance for black leaves
        diffuse_extinction_coefficient: [m2ground m-2leaf] the extinction coefficient of diffuse irradiance

    Returns:
        [W m-2ground] the absorbed irradiance by shaded leaves of a leaf layer per unit ground area
    """

    absorbed_diffuse_irradiance = calc_absorbed_diffuse_irradiance_per_leaf_layer(
        incident_diffuse_irradiance,
        upper_cumulative_leaf_area_index,
        leaf_layer_thickness,
        canopy_reflectance_to_diffuse_irradiance,
        diffuse_extinction_coefficient)

    absorbed_scattered_irradiance = calc_absorbed_scattered_irradiance_per_leaf_layer(
        incident_direct_irradiance,
        upper_cumulative_leaf_area_index,
        leaf_layer_thickness,
        direct_extinction_coefficient,
        direct_black_extinction_coefficient,
        canopy_reflectance_to_direct_irradiance,
        leaf_scattering_coefficient)

    shaded_area = leaf_layer_thickness * (1.0 - calc_sunlit_fraction_per_leaf_layer(
        upper_cumulative_leaf_area_index, leaf_layer_thickness, direct_black_extinction_coefficient))

    return (absorbed_diffuse_irradiance + absorbed_scattered_irradiance) * shaded_area
