from numpy import arange, testing
from crop_irradiance.formalisms import lumped_leaves


def test_calc_beer_absorption_is_greater_to_zero_for_none_zero_incident_irradiance():
    leaf_area_index = 3.0
    extinction_coefficient = 0.5
    incident_irradiance = 500
    assert lumped_leaves.calc_beer_absorption(incident_irradiance, extinction_coefficient, leaf_area_index) > 0


def test_calc_beer_absorption_is_equal_to_expected_values():
    leaf_area_index = 3.0
    extinction_coefficient = 0.5
    incident_irradiance = 500
    obtained_result = lumped_leaves.calc_beer_absorption(incident_irradiance, extinction_coefficient, leaf_area_index)
    expected_result = 388.435
    testing.assert_almost_equal(obtained_result, expected_result, decimal=3)


def test_calc_beer_absorption_increases_as_leaf_area_index_increases():
    extinction_coefficient = 0.5
    incident_irradiance = 500
    absorbed_irradiance = [
        lumped_leaves.calc_beer_absorption(incident_irradiance, extinction_coefficient, leaf_area_index) for
        leaf_area_index in arange(0, 5, 0.1)]
    assert all([x < y for x, y in zip(absorbed_irradiance, absorbed_irradiance[1:])])


def test_calc_beer_absorption_increases_as_extinction_coefficient_increases():
    leaf_area_index = 3.0
    incident_irradiance = 500
    absorbed_irradiance = [
        lumped_leaves.calc_beer_absorption(incident_irradiance, extinction_coefficient, leaf_area_index) for
        extinction_coefficient in arange(0, 2, 0.1)]
    assert all([x < y for x, y in zip(absorbed_irradiance, absorbed_irradiance[1:])])
