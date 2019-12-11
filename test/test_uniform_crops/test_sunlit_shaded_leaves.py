from numpy import testing, linspace, pi
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

