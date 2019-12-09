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
    return leaves_to_sun_average_projection / sin(solar_inclination)


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


def calc_diffuse_extinction_coefficient(leaf_area_index: float,
                                        leaf_scattering_coefficient: float,
                                        sky_sectors_number: int = 3) -> (float, float):
    """Calculates the diffuse extinction coefficients for canopies with non-black and black leaves.

    Args:
        leaf_area_index: [m2leaf m-2ground] leaf area index of the whole canopy
        leaf_scattering_coefficient: [-] leaf scattering coefficient
        sky_sectors_number: [-] number of sky sectors to be used

    Returns:
        [m2ground m-2leaf] the extinction coefficient of diffuse irradiance through a canopy of non-black leaves
        [m2ground m-2leaf] the extinction coefficient of diffuse irradiance through a canopy of black leaves

    References:
        Goudriaan J. (1988)
        The bare bones of leaf-angle distribution in radiation models for canopy photosynthesis and energy exchange.
        Agricultural and Forest Meteorology 43, 155 - 169.
    """
    angle_increment = (pi / 2.0) / sky_sectors_number / 2.0  # half increment in sky ring declination angle

    k_dif = 0.0
    k_dif_black = 0.0

    for i in range(sky_sectors_number):
        beta_sky_i = angle_increment * (1.0 + 2.0 * i)
        beta_sky_l = i * 2.0 * angle_increment
        beta_sky_u = (i + 1) * 2.0 * angle_increment
        # Weight factor for each sky ring, the value 7.0/6.0 results from integrating
        # c_sky_i over the sky hemisphere, thus used for normalization.
        c_sky_i = (sin(beta_sky_u) ** 2) * (0.5 + 2.0 / 3.0 * sin(beta_sky_u)) - (sin(beta_sky_l) ** 2) * (
                0.5 + 2.0 / 3.0 * (sin(beta_sky_l))) / (7.0 / 6.0)
        k_dif_i = c_sky_i * exp(-(0.5 / sin(beta_sky_i)) * sqrt(1.0 - leaf_scattering_coefficient) * leaf_area_index)
        k_dif += k_dif_i

        k_dif_i_black = c_sky_i * exp(-(0.5 / sin(beta_sky_i)) * leaf_area_index)
        k_dif_black += k_dif_i_black

    k_dif = -1.0 / leaf_area_index * log(k_dif)
    k_dif_black = -1.0 / leaf_area_index * log(k_dif_black)

    return k_dif, k_dif_black


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
