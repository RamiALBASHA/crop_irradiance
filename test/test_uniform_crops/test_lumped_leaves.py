from numpy import arange, testing
from crop_irradiance.uniform_crops.formalisms import lumped_leaves


def test_calc_beer_absorption_is_greater_to_zero_for_none_zero_incident_irradiance():
    incident_irradiance = 500
    extinction_coefficient = 0.5
    upper_cumulative_leaf_area_index = 3.0
    leaf_layer_thickness = 0.5
    assert lumped_leaves.calc_beer_absorption(incident_irradiance, extinction_coefficient,
                                              upper_cumulative_leaf_area_index, leaf_layer_thickness) > 0


def test_calc_beer_absorption_is_equal_to_expected_values():
    incident_irradiance = 500
    extinction_coefficient = 0.5
    upper_cumulative_leaf_area_index = 0.0
    leaf_layer_thickness = 3.0
    obtained_result = lumped_leaves.calc_beer_absorption(incident_irradiance, extinction_coefficient,
                                                         upper_cumulative_leaf_area_index, leaf_layer_thickness)
    expected_result = 388.435
    testing.assert_almost_equal(obtained_result, expected_result, decimal=3)


def test_calc_beer_absorption_increases_as_leaf_area_index_increases():
    incident_irradiance = 500
    extinction_coefficient = 0.5
    upper_cumulative_leaf_area_index = 0.0
    absorbed_irradiance = [
        lumped_leaves.calc_beer_absorption(incident_irradiance, extinction_coefficient,
                                           upper_cumulative_leaf_area_index, leaf_layer_thickness) for
        leaf_layer_thickness in arange(0, 5, 0.1)]
    assert all([x < y for x, y in zip(absorbed_irradiance, absorbed_irradiance[1:])])


def test_calc_beer_absorption_increases_as_extinction_coefficient_increases():
    incident_irradiance = 500
    upper_cumulative_leaf_area_index = 0.0
    leaf_layer_thickness = 3.0
    absorbed_irradiance = [
        lumped_leaves.calc_beer_absorption(incident_irradiance, extinction_coefficient,
                                           upper_cumulative_leaf_area_index, leaf_layer_thickness) for
        extinction_coefficient in arange(0, 2, 0.1)]
    assert all([x < y for x, y in zip(absorbed_irradiance, absorbed_irradiance[1:])])
