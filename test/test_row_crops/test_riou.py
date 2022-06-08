from math import radians

from pytest import fixture

from crop_irradiance.row_crops.formalisms.riou import calc_riou89
from test.utils import assert_values_trend


@fixture()
def common_inputs():
    return dict(
        row_width=0.3,
        row_spacing=1.8,
        canopy_height=0.9,
        solar_inclination=radians(60),
        solar_azimuth=radians(45),
        normal_angle_row=radians(90),
        porosity=1 / 3,
        incident_direct_irradiance=500,
        incident_diffuse_irradiance=200,
        albedo_leaves=0.2,
        albedo_soil=0.18)


def test_calc_riou89_returns_zero_when_during_night(common_inputs):
    common_inputs.update({'incident_direct_irradiance': 0, 'incident_diffuse_irradiance': 0})
    assert calc_riou89(**common_inputs) == 0


def test_calc_absorbed_irradiance_increases_as_row_width_increases(common_inputs):
    abs_irradiance = []
    for x in range(1, 11):
        common_inputs.update({'row_width': x / 10})
        abs_irradiance.append(calc_riou89(**common_inputs))
    assert_values_trend(values=abs_irradiance, trend='+')


def test_calc_absorbed_irradiance_increases_as_row_height_increases(common_inputs):
    abs_irradiance = []
    for x in range(1, 11):
        common_inputs.update({'canopy_height': x / 10})
        abs_irradiance.append(calc_riou89(**common_inputs))
    assert_values_trend(values=abs_irradiance, trend='+')


def test_calc_absorbed_irradiance_decreases_as_porosity_increases(common_inputs):
    abs_irradiance = []
    for x in range(1, 10):
        common_inputs.update({'porosity': x / 10})
        abs_irradiance.append(calc_riou89(**common_inputs))
    assert_values_trend(values=abs_irradiance, trend='-')


def test_calc_absorbed_irradiance_increases_as_solar_beam_approaches_the_normal_to_the_row_axis(common_inputs):
    abs_irradiance = []
    for a in range(0, 91):
        common_inputs.update({'solar_azimuth': radians(a)})
        abs_irradiance.append(calc_riou89(**common_inputs))
    assert_values_trend(values=abs_irradiance, trend='+')


def test_calc_absorbed_irradiance_is_maximum_at_solar_noon_for_east_west_rows(common_inputs):
    common_inputs.update({'normal_angle_row': radians(0), 'solar_azimuth': radians(90)})

    abs_irradiance = []
    for a in range(0, 180, 5):
        common_inputs.update({'solar_inclination': radians(a)})
        abs_irradiance.append(calc_riou89(**common_inputs))
    assert_values_trend(values=abs_irradiance[:18], trend='+')
    assert_values_trend(values=abs_irradiance[18:], trend='-')
