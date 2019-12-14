from math import exp


def calc_beer_absorption(incident_irradiance: float, extinction_coefficient: float, leaf_area_index: float) -> float:
    """Calculates irradiance absorption by a uniform leaf layer following Beer-Lambert's law.

    Parameters
    ----------
    incident_irradiance: [W m-2ground] incident irradiance at the upper side of the leaf layer
    extinction_coefficient: [m2groud m-2leaf] extinction coefficient of the incident irradiance through the canopy
    leaf_area_index: [m2leaf m-2ground] leaf area per unit ground area

    Returns
    -------
    [W m-2ground] absorbed irradiance per unit ground area

    Notes
    -----
    The unit of the incident irradiance given above may be set differently by the user (e.g. J cm-2ground), in which
        case the absorbed irradiance will have the same unit (e.g. J cm-2ground)
    """
    absorbed_fraction = 1.0 - exp(- extinction_coefficient * leaf_area_index)
    return incident_irradiance * absorbed_fraction
