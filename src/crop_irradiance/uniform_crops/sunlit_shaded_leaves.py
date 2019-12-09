from math import exp


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
