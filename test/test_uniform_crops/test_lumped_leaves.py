from crop_irradiance.uniform_crops.formalisms import lumped_leaves
from numpy import arange, testing


def assert_values_trend(values: list, trend: str) -> None or AssertionError:
    """Asserts that a vector of values follows a given trend

    Args:
        values: values whose trend is to be checked
        trend: one of ('increasing', 'decreasing', 'non-monotonic')
    """
    if trend == 'increasing':
        assert all([x <= y for x, y in zip(values, values[1:])])
    elif trend == 'decreasing':
        assert all([x >= y for x, y in zip(values, values[1:])])
    elif trend == 'non-monotonic':
        assert (not all([x <= y for x, y in zip(values, values[1:])]) and
                not all([x >= y for x, y in zip(values, values[1:])]))


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


def test_calc_absorbed_direct_irradiance_is_positive():
    incident_direct_irradiance = 500
    upper_cumulative_leaf_area_index = 0
    leaf_layer_thickness = 3
    direct_extinction_coefficient = 0.5
    canopy_reflectance_to_direct_irradiance = 0.027
    assert 0 <= lumped_leaves.calc_absorbed_direct_irradiance(incident_direct_irradiance,
                                                              upper_cumulative_leaf_area_index,
                                                              leaf_layer_thickness,
                                                              direct_extinction_coefficient,
                                                              canopy_reflectance_to_direct_irradiance)


def test_calc_absorbed_direct_irradiance_increases_as_incident_direct_irradiance_increases():
    upper_cumulative_leaf_area_index = 0
    leaf_layer_thickness = 3
    direct_extinction_coefficient = 0.5
    canopy_reflectance_to_direct_irradiance = 0.027
    absorbed_irradiance = [lumped_leaves.calc_absorbed_direct_irradiance(incident_direct_irradiance,
                                                                         upper_cumulative_leaf_area_index,
                                                                         leaf_layer_thickness,
                                                                         direct_extinction_coefficient,
                                                                         canopy_reflectance_to_direct_irradiance)
                           for incident_direct_irradiance in range(0, 800, 100)]

    assert_values_trend(values=absorbed_irradiance, trend='increasing')


def test_calc_absorbed_direct_irradiance_increases_as_leaf_area_index_increases():
    incident_direct_irradiance = 500
    upper_cumulative_leaf_area_index = 0
    direct_extinction_coefficient = 0.5
    canopy_reflectance_to_direct_irradiance = 0.027
    absorbed_irradiance = [lumped_leaves.calc_absorbed_direct_irradiance(incident_direct_irradiance,
                                                                         upper_cumulative_leaf_area_index,
                                                                         leaf_layer_thickness,
                                                                         direct_extinction_coefficient,
                                                                         canopy_reflectance_to_direct_irradiance)
                           for leaf_layer_thickness in range(0, 10, 1)]

    assert_values_trend(values=absorbed_irradiance, trend='increasing')


def test_calc_absorbed_direct_irradiance_increases_as_direct_extinction_coefficient_increases():
    incident_direct_irradiance = 500
    upper_cumulative_leaf_area_index = 0
    leaf_layer_thickness = 3
    canopy_reflectance_to_direct_irradiance = 0.027
    absorbed_irradiance = [lumped_leaves.calc_absorbed_direct_irradiance(incident_direct_irradiance,
                                                                         upper_cumulative_leaf_area_index,
                                                                         leaf_layer_thickness,
                                                                         direct_extinction_coefficient,
                                                                         canopy_reflectance_to_direct_irradiance)
                           for direct_extinction_coefficient in arange(0, 15, 0.1)]

    assert_values_trend(values=absorbed_irradiance, trend='increasing')


def test_calc_absorbed_direct_irradiance_decreases_as_canopy_reflectance_to_direct_irradiance_increases():
    incident_direct_irradiance = 500
    upper_cumulative_leaf_area_index = 0
    leaf_layer_thickness = 3
    direct_extinction_coefficient = 0.5
    absorbed_irradiance = [lumped_leaves.calc_absorbed_direct_irradiance(incident_direct_irradiance,
                                                                         upper_cumulative_leaf_area_index,
                                                                         leaf_layer_thickness,
                                                                         direct_extinction_coefficient,
                                                                         canopy_reflectance_to_direct_irradiance)
                           for canopy_reflectance_to_direct_irradiance in arange(0, 15, 0.1)]

    assert_values_trend(values=absorbed_irradiance, trend='decreasing')


def test_calc_absorbed_diffuse_irradiance_is_positive():
    incident_diffuse_irradiance = 100
    upper_cumulative_leaf_area_index = 0
    leaf_layer_thickness = 3
    diffuse_extinction_coefficient = 0.64
    canopy_reflectance_to_diffuse_irradiance = 0.057

    assert 0 <= lumped_leaves.calc_absorbed_diffuse_irradiance(incident_diffuse_irradiance,
                                                               upper_cumulative_leaf_area_index,
                                                               leaf_layer_thickness,
                                                               diffuse_extinction_coefficient,
                                                               canopy_reflectance_to_diffuse_irradiance)


def test_calc_absorbed_diffuse_irradiance_increases_as_incident_diffuse_irradiance_increases():
    upper_cumulative_leaf_area_index = 0
    leaf_layer_thickness = 3
    diffuse_extinction_coefficient = 0.64
    canopy_reflectance_to_diffuse_irradiance = 0.057

    absorbed_irradiance = [lumped_leaves.calc_absorbed_diffuse_irradiance(incident_diffuse_irradiance,
                                                                          upper_cumulative_leaf_area_index,
                                                                          leaf_layer_thickness,
                                                                          diffuse_extinction_coefficient,
                                                                          canopy_reflectance_to_diffuse_irradiance)
                           for incident_diffuse_irradiance in range(0, 100, 10)]

    assert_values_trend(values=absorbed_irradiance, trend='increasing')


def test_calc_absorbed_diffuse_irradiance_increases_as_leaf_area_index_increases():
    incident_diffuse_irradiance = 100
    upper_cumulative_leaf_area_index = 0
    diffuse_extinction_coefficient = 0.64
    canopy_reflectance_to_diffuse_irradiance = 0.057

    absorbed_irradiance = [lumped_leaves.calc_absorbed_diffuse_irradiance(incident_diffuse_irradiance,
                                                                          upper_cumulative_leaf_area_index,
                                                                          leaf_layer_thickness,
                                                                          diffuse_extinction_coefficient,
                                                                          canopy_reflectance_to_diffuse_irradiance)
                           for leaf_layer_thickness in range(0, 10)]

    assert_values_trend(values=absorbed_irradiance, trend='increasing')


def test_calc_absorbed_diffuse_irradiance_increases_as_diffuse_extinction_coefficient_increases():
    incident_diffuse_irradiance = 100
    upper_cumulative_leaf_area_index = 0
    leaf_layer_thickness = 3
    diffuse_extinction_coefficient = 0.64

    absorbed_irradiance = [lumped_leaves.calc_absorbed_diffuse_irradiance(incident_diffuse_irradiance,
                                                                          upper_cumulative_leaf_area_index,
                                                                          leaf_layer_thickness,
                                                                          diffuse_extinction_coefficient,
                                                                          canopy_reflectance_to_diffuse_irradiance)
                           for canopy_reflectance_to_diffuse_irradiance in arange(0, 0.5, 0.01)]

    assert_values_trend(values=absorbed_irradiance, trend='decreasing')


def test_calc_de_pury_absorption_is_positive():
    incident_direct_irradiance = 500
    incident_diffuse_irradiance = 100
    upper_cumulative_leaf_area_index = 0
    leaf_layer_thickness = 3
    direct_extinction_coefficient = 0.5
    diffuse_extinction_coefficient = 0.64
    canopy_reflectance_to_direct_irradiance = 0.027
    canopy_reflectance_to_diffuse_irradiance = 0.057

    assert 0 <= lumped_leaves.calc_de_pury_absorption(incident_direct_irradiance,
                                                      incident_diffuse_irradiance,
                                                      upper_cumulative_leaf_area_index,
                                                      leaf_layer_thickness,
                                                      direct_extinction_coefficient,
                                                      diffuse_extinction_coefficient,
                                                      canopy_reflectance_to_direct_irradiance,
                                                      canopy_reflectance_to_diffuse_irradiance)
