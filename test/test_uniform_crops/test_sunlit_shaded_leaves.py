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
