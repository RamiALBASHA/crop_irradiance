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
