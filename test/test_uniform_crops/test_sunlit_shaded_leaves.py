from numpy import testing, linspace, pi, arange, random
from crop_irradiance.uniform_crops import sunlit_shaded_leaves


def test_calc_leaf_scattering_coefficient_returns_expected_values():
    testing.assert_almost_equal(sunlit_shaded_leaves.calc_leaf_scattering_coefficient(0.08, 0.07), 0.15, decimal=3)


def test_calc_direct_black_extinction_coefficient_is_maximum_at_sunrise_and_sunset():
    extinction_coef_at_sunrise = sunlit_shaded_leaves.calc_direct_black_extinction_coefficient(0.0, 0.5)
    extinction_coef_at_midday = sunlit_shaded_leaves.calc_direct_black_extinction_coefficient(pi / 2.0, 0.5)
    extinction_coef_at_sunset = sunlit_shaded_leaves.calc_direct_black_extinction_coefficient(pi, 0.5)

    assert extinction_coef_at_sunrise > extinction_coef_at_midday
    assert extinction_coef_at_sunset > extinction_coef_at_midday


def test_calc_direct_extinction_coefficient_is_zero_when_leaf_scattering_is_unity():
    leaf_scattering_coefficient = 1.
    solar_inclination = pi / 3.
    assert sunlit_shaded_leaves.calc_direct_extinction_coefficient(solar_inclination, leaf_scattering_coefficient) == 0.


def test_calc_direct_extinction_coefficient_returns_expected_value():
    leaf_scattering_coefficient = 0.15
    solar_inclination = pi / 2.
    expected_value = 0.4609772228646444
    actual_value = sunlit_shaded_leaves.calc_direct_extinction_coefficient(solar_inclination,
                                                                           leaf_scattering_coefficient)
    testing.assert_almost_equal(actual_value, expected_value, decimal=6)


def test_calc_sky_sectors_weight_returns_expected_uoc_values():
    assert sunlit_shaded_leaves.calc_sky_sectors_weight(3, 'uoc') == [0.25, 0.5, 0.25]


def test_calc_sky_sectors_weight_returns_expected_soc_values():
    actual_values = sunlit_shaded_leaves.calc_sky_sectors_weight(3, 'soc')
    expected_values = [0.1785714285714285, 0.5140108873361879, 0.3074176840923834]
    testing.assert_almost_equal(actual_values, expected_values, decimal=6)


def test_calc_sky_sectors_weight_returns_empty_list_for_unknown_sky_type():
    assert sunlit_shaded_leaves.calc_sky_sectors_weight(3, 'some unkonwn sky type') == []


def test_calc_sky_sectors_weight_returns_weights_which_sums_up_to_1():
    for sky_type in ('soc', 'uoc'):
        actual_value = sum(sunlit_shaded_leaves.calc_sky_sectors_weight(3, sky_type))
        expected_value = 1.0
        testing.assert_almost_equal(actual_value, expected_value, decimal=6)


def test_calc_diffuse_extinction_coefficient_reduces_as_leaf_area_index_increases():
    leaf_scattering_coefficient = 0.15
    diffuse_coeffcients = [
        sunlit_shaded_leaves.calc_diffuse_extinction_coefficient(leaf_area_index, leaf_scattering_coefficient) for
        leaf_area_index in arange(0, 5.1, 0.1)]
    assert all([x > y for x, y in zip(diffuse_coeffcients, diffuse_coeffcients[1:])])


def test_calc_diffuse_extinction_coefficient_returns_greater_extinction_coefficient_for_black_leaves():
    leaf_area_index = 3.0
    leaf_scattering_coefficient = 0.15
    sky_sectors_number = 3
    for sky_type in ('soc', 'uoc'):
        extinction_coef, black_extinction_coef = sunlit_shaded_leaves.calc_diffuse_extinction_coefficient(
            leaf_area_index, leaf_scattering_coefficient, sky_sectors_number, sky_type)
    assert extinction_coef < black_extinction_coef


def test_calc_diffuse_extinction_coefficient_returns_expected_values():
    leaf_area_index = 3.0
    leaf_scattering_coefficient = 0.15
    sky_sectors_number = 3
    expected_values = {'soc': (0.6390947959070368, 0.6872841045179627),
                       'uoc': (0.675874154734713, 0.7250108165502616)}

    for sky_type in ('soc', 'uoc'):
        actual_values = sunlit_shaded_leaves.calc_diffuse_extinction_coefficient(
            leaf_area_index, leaf_scattering_coefficient, sky_sectors_number, sky_type)
    testing.assert_almost_equal(actual_values, expected_values[sky_type], decimal=6)


def test_calc_canopy_reflectance_to_direct_irradiance_is_zero_when_leaf_scattering_is_zero():
    assert sunlit_shaded_leaves.calc_canopy_reflectance_to_direct_irradiance(random.rand(), 0.) == 0.0


def test_calc_canopy_reflectance_to_direct_irradiance_increases_as_leaf_scattering_increases():
    canopy_reflectance = [sunlit_shaded_leaves.calc_canopy_reflectance_to_direct_irradiance(0.5, scattering_coef) for
                          scattering_coef in arange(0, 1.1, 0.1)]
    assert all([x < y for x, y in zip(canopy_reflectance, canopy_reflectance[1:])])


def test_calc_canopy_reflectance_to_direct_irradiance_increases_as_direct_black_extinction_coefficient_increases():
    canopy_reflectance = [sunlit_shaded_leaves.calc_canopy_reflectance_to_direct_irradiance(extinction_coef, 0.15) for
                          extinction_coef in arange(0, 1.1, 0.1)]
    assert all([x < y for x, y in zip(canopy_reflectance, canopy_reflectance[1:])])


def test_calc_canopy_reflectance_to_diffuse_irradiance_returns_expected_values_for_par_band():
    assert sunlit_shaded_leaves.get_canopy_reflectance_to_diffuse_irradiance('par') == 0.057


def test_calc_canopy_reflectance_to_diffuse_irradiance_returns_expected_values_for_nir_band():
    assert sunlit_shaded_leaves.get_canopy_reflectance_to_diffuse_irradiance('nir') == 0.389


def test_calc_canopy_reflectance_to_diffuse_irradiance_raises_error_for_unexpected_irradiance_bands():
    try:
        sunlit_shaded_leaves.get_canopy_reflectance_to_diffuse_irradiance('some unexpected band')
    except ValueError as e:
        assert e.args[0] == '"irradiance_band" must be one of ("par", "nir")'


def test_calc_sunlit_fraction_decreases_as_cumulative_leaf_area_index_increases():
    sunlit_fraction = [sunlit_shaded_leaves.calc_sunlit_fraction(cumulative_leaf_area_index, 0.5) for
                       cumulative_leaf_area_index in arange(0, 5, 0.1)]
    assert all([x > y for x, y in zip(sunlit_fraction, sunlit_fraction[1:])])


def test_calc_sunlit_fraction_decreases_as_extinction_coefficient_increases():
    sunlit_fraction = [sunlit_shaded_leaves.calc_sunlit_fraction(3., extinction_coef) for
                       extinction_coef in arange(0.5, 10.5, 0.5)]
    assert all([x > y for x, y in zip(sunlit_fraction, sunlit_fraction[1:])])


def test_calc_shaded_fraction_increases_as_cumulative_leaf_area_index_increases():
    sunlit_fraction = [sunlit_shaded_leaves.calc_shaded_fraction(cumulative_leaf_area_index, 0.5) for
                       cumulative_leaf_area_index in arange(0, 5, 0.1)]
    assert all([x < y for x, y in zip(sunlit_fraction, sunlit_fraction[1:])])


def test_calc_shadedfraction_increases_as_direct_black_extinction_coefficient_increases():
    sunlit_fraction = [sunlit_shaded_leaves.calc_shaded_fraction(3., extinction_coef) for
                       extinction_coef in arange(0.5, 10.5, 0.5)]
    assert all([x < y for x, y in zip(sunlit_fraction, sunlit_fraction[1:])])


def test_calc_absorbed_direct_irradiance_increases_as_incident_direct_irradiance_increases():
    absorbed_irradiance = [sunlit_shaded_leaves.calc_absorbed_direct_irradiance(incident_direct_irradiance, 0.15, 0.5)
                           for incident_direct_irradiance in range(0, 800, 100)]
    assert all([x < y for x, y in zip(absorbed_irradiance, absorbed_irradiance[1:])])


def test_calc_absorbed_direct_irradiance_decreases_as_leaf_scattering_coefficient_decreases():
    absorbed_irradiance = [sunlit_shaded_leaves.calc_absorbed_direct_irradiance(800., leaf_scattering, 0.5)
                           for leaf_scattering in arange(0, 1.1, 0.1)]
    assert all([x > y for x, y in zip(absorbed_irradiance, absorbed_irradiance[1:])])


def test_calc_absorbed_direct_irradiance_increases_as_direct_black_extinction_coefficient_increases():
    absorbed_irradiance = [sunlit_shaded_leaves.calc_absorbed_direct_irradiance(800., 0.15, extinction_coef) for
                           extinction_coef in arange(0.5, 10.5, 0.5)]
    assert all([x < y for x, y in zip(absorbed_irradiance, absorbed_irradiance[1:])])


def test_calc_absorbed_diffuse_irradiance_at_given_depth_increases_as_incident_diffuse_irradiance_increases():
    absorbed_irradiance = [
        sunlit_shaded_leaves.calc_absorbed_diffuse_irradiance_at_given_depth(
            incident_diffuse_irradiance, 3.0, 0.4, 0.64) for incident_diffuse_irradiance in range(0, 80, 10)]
    assert all([x < y for x, y in zip(absorbed_irradiance, absorbed_irradiance[1:])])


def test_calc_absorbed_diffuse_irradiance_at_given_depth_decreases_as_cumulative_leaf_area_index_increases():
    absorbed_irradiance = [
        sunlit_shaded_leaves.calc_absorbed_diffuse_irradiance_at_given_depth(10., cumulative_leaf_area_index, 0.4, 0.64)
        for cumulative_leaf_area_index in arange(0, 5, 0.1)]
    assert all([x > y for x, y in zip(absorbed_irradiance, absorbed_irradiance[1:])])


def test_calc_absorbed_diffuse_irradiance_at_given_depth_decreases_as_canopy_reflectance_increases():
    absorbed_irradiance = [
        sunlit_shaded_leaves.calc_absorbed_diffuse_irradiance_at_given_depth(10., 3.0, canopy_reflectance, 0.64)
        for canopy_reflectance in arange(0, 1.1, 0.1)]
    assert all([x > y for x, y in zip(absorbed_irradiance, absorbed_irradiance[1:])])


def test_calc_absorbed_diffuse_irradiance_at_given_depth_does_not_have_monotonic_trend_with_diffuse_extinction_coef():
    absorbed_irradiance = [sunlit_shaded_leaves.calc_absorbed_diffuse_irradiance_at_given_depth(
        10., 3.0, 0.4, diffuse_extinction_coefficient) for diffuse_extinction_coefficient in arange(0, 1.1, 0.1)]
    assert not all([x < y for x, y in zip(absorbed_irradiance, absorbed_irradiance[1:])])


def test_calc_absorbed_diffuse_irradiance_at_given_depth_peaks_at_predefined_value():
    absorbed_irradiance = [sunlit_shaded_leaves.calc_absorbed_diffuse_irradiance_at_given_depth(
        10., 3.0, 0.4, diffuse_extinction_coefficient) for diffuse_extinction_coefficient in arange(0, 1.1, 0.1)]
    absorbed_irradiance_max = absorbed_irradiance[3]
    assert all([abs_irradiance <= absorbed_irradiance_max for abs_irradiance in absorbed_irradiance])
