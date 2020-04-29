from math import exp


def calc_beer_absorption(incident_irradiance: float,
                         extinction_coefficient: float,
                         upper_cumulative_leaf_area_index: float,
                         leaf_layer_thickness: float) -> float:
    """Calculates irradiance absorption by a uniform leaf layer following Beer-Lambert's law.

    Args:
        incident_irradiance: [W m-2ground] incident irradiance at the upper side of the leaf layer
        extinction_coefficient: [m2groud m-2leaf] extinction coefficient of the incident irradiance through the canopy
        upper_cumulative_leaf_area_index: [m2leaf m-2ground] cumulative downwards leaf area index at the top of the
            considered layer
        leaf_layer_thickness: [m2leaf m-2ground] leaf area index of the considered layer

    Returns:
        [W m-2ground] absorbed irradiance per unit ground area

    Notes
        The unit of the incident irradiance given above may be set differently by the user (e.g. J cm-2ground), in
            which case the absorbed irradiance will have the same unit (e.g. J cm-2ground)

    """
    scaling_factor = (
            exp(-extinction_coefficient * upper_cumulative_leaf_area_index) -
            exp(-extinction_coefficient * (upper_cumulative_leaf_area_index + leaf_layer_thickness)))

    return incident_irradiance * scaling_factor


def calc_de_pury_absorption(incident_direct_irradiance: float,
                            incident_diffuse_irradiance: float,
                            upper_cumulative_leaf_area_index: float,
                            leaf_layer_thickness: float,
                            direct_extinction_coefficient: float,
                            diffuse_extinction_coefficient: float,
                            canopy_reflectance_to_direct_irradiance: float,
                            canopy_reflectance_to_diffuse_irradiance: float) -> float:
    """Calculates the absorbed direct and diffuse irradiance by a leaf layer per unit ground area.

    Args:
        incident_direct_irradiance: [W m-2ground] incident direct (beam) irradiance at the top of the canopy
        incident_diffuse_irradiance: [W m-2ground] incident diffuse irradiance at the top of the canopy
        upper_cumulative_leaf_area_index: [m2leaf m-2ground] cumulative downwards leaf area index at the top of the
            considered layer
        leaf_layer_thickness: [m2leaf m-2ground] leaf area index of the considered layer
        direct_extinction_coefficient: [m2ground m-2leaf] the extinction coefficient of direct (beam) irradiance
        diffuse_extinction_coefficient: [m2ground m-2leaf] the extinction coefficient of diffuse irradiance
        canopy_reflectance_to_direct_irradiance: [-] canopy reflectance to direct (beam) irradiance
        canopy_reflectance_to_diffuse_irradiance: [-] canopy reflectance to diffuse irradiance for the given irradiance
            band

    Returns:
        [W m-2ground]: the absorbed direct and diffuse irradiance by a leaf layer per unit ground area

    """
    absorbed_direct_irradiance = calc_absorbed_direct_irradiance(incident_direct_irradiance,
                                                                 upper_cumulative_leaf_area_index,
                                                                 leaf_layer_thickness,
                                                                 direct_extinction_coefficient,
                                                                 canopy_reflectance_to_direct_irradiance)

    absorbed_diffuse_irradiance = calc_absorbed_diffuse_irradiance(incident_diffuse_irradiance,
                                                                   upper_cumulative_leaf_area_index,
                                                                   leaf_layer_thickness,
                                                                   diffuse_extinction_coefficient,
                                                                   canopy_reflectance_to_diffuse_irradiance)

    return absorbed_direct_irradiance + absorbed_diffuse_irradiance


def calc_absorbed_direct_irradiance(incident_direct_irradiance: float,
                                    upper_cumulative_leaf_area_index: float,
                                    leaf_layer_thickness: float,
                                    direct_extinction_coefficient: float,
                                    canopy_reflectance_to_direct_irradiance: float) -> float:
    """Calculates the absorbed direct irradiance by a leaf layer per unit ground area.

    Args:
        incident_direct_irradiance: [W m-2ground] incident direct (beam) irradiance at the top of the canopy
        upper_cumulative_leaf_area_index: [m2leaf m-2ground] cumulative downwards leaf area index at the top of the
            considered layer
        leaf_layer_thickness: [m2leaf m-2ground] leaf area index of the considered layer
        direct_extinction_coefficient: [m2ground m-2leaf] the extinction coefficient of direct (beam) irradiance
        canopy_reflectance_to_direct_irradiance: [-] canopy reflectance to direct (beam) irradiance

    Returns:
        [W m-2ground] the absorbed direct irradiance by a leaf layer per unit ground area
    """

    scaling_factor = (
            exp(-direct_extinction_coefficient * upper_cumulative_leaf_area_index) -
            exp(-direct_extinction_coefficient * (upper_cumulative_leaf_area_index + leaf_layer_thickness)))

    return incident_direct_irradiance * (1 - canopy_reflectance_to_direct_irradiance) * scaling_factor


def calc_absorbed_diffuse_irradiance(incident_diffuse_irradiance: float,
                                     upper_cumulative_leaf_area_index: float,
                                     leaf_layer_thickness: float,
                                     diffuse_extinction_coefficient: float,
                                     canopy_reflectance_to_diffuse_irradiance: float) -> float:
    """Calculates the absorbed diffuse irradiance by a leaf layer per unit ground area.

    Args:
        incident_diffuse_irradiance: [W m-2ground] incident diffuse irradiance at the top of the canopy
        upper_cumulative_leaf_area_index: [m2leaf m-2ground] cumulative downwards leaf area index at the top of the
            considered layer
        leaf_layer_thickness: [m2leaf m-2ground] leaf area index of the considered layer
        diffuse_extinction_coefficient: [m2ground m-2leaf] the extinction coefficient of diffuse irradiance
        canopy_reflectance_to_diffuse_irradiance: [-] canopy reflectance to diffuse irradiance for the given irradiance
            band

    Returns:
        [W m-2ground] the absorbed diffuse irradiance by a leaf layer per unit ground area

    """
    scaling_factor = (
            exp(-diffuse_extinction_coefficient * upper_cumulative_leaf_area_index) -
            exp(-diffuse_extinction_coefficient * (upper_cumulative_leaf_area_index + leaf_layer_thickness)))

    return incident_diffuse_irradiance * (1 - canopy_reflectance_to_diffuse_irradiance) * scaling_factor
