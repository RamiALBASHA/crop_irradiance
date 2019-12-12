from numpy import testing, linspace, pi, arange
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
