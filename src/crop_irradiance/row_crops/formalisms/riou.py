from math import cos, tan, sin, atan
from crop_irradiance.config import PRECISION


def calc_riou89(row_width: float, row_spacing: float, canopy_height: float, solar_inclination: float,
                solar_azimuth: float, normal_angle_row: float, porosity: float,
                incident_direct_irradiance: float, incident_diffuse_irradiance: float,
                albedo_leaves: float, albedo_soil: float) -> float:
    """Calculates absorbed irradiance by a grapevine trained on a VSP (Vertical Shoot Positioning) system.

    Args:
        row_width: [m] row width
        row_spacing: [m] spacing between the axis of two adjacent rows
        canopy_height: [m] height of the part of the canopy that is covered by leaves
        solar_inclination: (rad) solar inclination angle (0 at horizon)
        solar_azimuth: (rad) solar azimuth angle (0 at South, pi/2 on East or West)
        normal_angle_row: (rad) angle between the normal to the row and the South (0 at South, pi/2 on East or West)
        porosity: [-] gaps fraction in the VERTICAL walls of the row
        incident_direct_irradiance: [W m-2] incident direct irradiance
        incident_diffuse_irradiance: [W m-2] incident diffuse irradiance
        albedo_leaves: [-] fraction of irradiance that is reflected by the vegetation surface
        albedo_soil: [-] fraction of irradiance that is reflected by the soil surface

    Returns:
        [W m-2] absorbed irradiance by 1 m of the crop row


    Notes:
        The unit of 'incident_direct_irradiance' and 'incident_diffuse_irradiance' can be any other irradiance unit,
        provided that both inputs has the same unit.

    Reference:
        Riou et al. (1989).
            Un modèle simple d’interception du rayonnement solaire par la vigne - vérification expérimentale.
            Agronomie: 9, 441 - 450.

    """

    if incident_direct_irradiance + incident_diffuse_irradiance == 0:
        res = 0
    else:
        solar_inclination = max(PRECISION, solar_inclination)
        res = _calc_riou_89(
            l=row_width,
            d=row_spacing,
            h=canopy_height,
            theta_h=solar_inclination,
            a=solar_azimuth,
            a_prime=normal_angle_row,
            p=porosity,
            incident_direct_irradiance=incident_direct_irradiance,
            incident_diffuse_irradiance=incident_diffuse_irradiance,
            a_f=albedo_leaves,
            a_s=albedo_soil)
    return res


def _calc_riou_89(l: float, d: float, h: float, theta_h: float, a: float, a_prime: float, p: float,
                  incident_direct_irradiance: float, incident_diffuse_irradiance: float,
                  a_f: float, a_s: float) -> float:
    i_v = incident_direct_irradiance * cos(theta_h) * cos(a - a_prime)
    i_h = incident_direct_irradiance * sin(theta_h)
    lambda_coef = i_v / i_h

    if lambda_coef <= l / h:
        i_abs_direct = i_h / d * (lambda_coef * h + l)
    elif lambda_coef <= (d - l) / h:
        i_abs_direct = i_h / d * (
                lambda_coef * h + l - p * (lambda_coef * h - l))
    elif lambda_coef <= d / h:
        i_abs_direct = i_h / d * (d - p * (lambda_coef * h - l))
    elif lambda_coef <= (d + l) / h:
        i_abs_direct = i_h / d * (d - p * (2 * d - l - lambda_coef * h))
    elif lambda_coef <= (2 * d - l) / h:
        i_abs_direct = i_h / d * (d - p * (2 * d - l - lambda_coef * h) - (p ** 2 * (lambda_coef * h - d - l)))
    # elif lambda_coef <= 3 * ex / H:
    else:
        i_abs_direct = i_h / d * (d - p ** 3 * (d - l))

    i0 = atan((d - l) / h)
    nh = (d - l) / d * (1 - tan(i0 / 2.))

    h1 = atan((2 * h) / l * sin(a))
    h2 = atan(h / (d - l / 2.) * sin(a))
    nl = 2 * l / d * ((sin(h1 / 2)) ** 2 - (sin(h2 / 2.)) ** 2)
    nd = (1 - p) * nh + l / d + p * nl

    i_abs_diffuse = nd * incident_diffuse_irradiance
    r_i = i_abs_direct + i_abs_diffuse
    return (1. - a_f) * r_i + a_s * nd * (1. - a_f) * (
            incident_direct_irradiance + incident_diffuse_irradiance - r_i)
