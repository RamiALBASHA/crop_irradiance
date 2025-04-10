from numpy import arange, pi, random, testing

from crop_irradiance.uniform_crops.formalisms import sunlit_shaded_leaves


def assert_values_trend(values: list, trend: str) -> None or AssertionError:
    """Asserts that a vector of values follows a given trend

    Args:
        values: values whose trend is to be checked
        trend: one of ('increasing', 'decreasing', 'non-monotonic')
    """
    if trend == "increasing":
        assert all([x < y for x, y in zip(values, values[1:])])
    elif trend == "decreasing":
        assert all([x > y for x, y in zip(values, values[1:])])
    elif trend == "non-monotonic":
        assert not all([x <= y for x, y in zip(values, values[1:])]) and not all(
            [x >= y for x, y in zip(values, values[1:])]
        )


def test_calc_leaf_scattering_coefficient_returns_expected_values():
    testing.assert_almost_equal(
        sunlit_shaded_leaves.calc_leaf_scattering_coefficient(0.08, 0.07),
        0.15,
        decimal=3,
    )


def test_calc_direct_black_extinction_coefficient_is_maximum_at_sunrise_and_sunset():
    extinction_coef_at_sunrise = (
        sunlit_shaded_leaves.calc_direct_black_extinction_coefficient(0.0, 0.9774, 1)
    )
    extinction_coef_at_midday = (
        sunlit_shaded_leaves.calc_direct_black_extinction_coefficient(
            pi / 2.0, 0.9774, 1
        )
    )
    extinction_coef_at_sunset = (
        sunlit_shaded_leaves.calc_direct_black_extinction_coefficient(pi, 0.9774, 1)
    )

    assert extinction_coef_at_sunrise > extinction_coef_at_midday
    assert extinction_coef_at_sunset > extinction_coef_at_midday


def test_calc_direct_black_extinction_coefficient_decreases_with_clumping():
    assert_values_trend(
        values=[
            sunlit_shaded_leaves.calc_direct_black_extinction_coefficient(
                0.0, 0.9774, c
            )
            for c in range(1, 0)
        ],
        trend="decreasing",
    )


def test_calc_direct_extinction_coefficient_is_zero_when_leaf_scattering_is_unity():
    leaf_scattering_coefficient = 1.0
    solar_inclination = pi / 3.0
    leaf_angle_distribution_factor = 0.9773843811168246
    clumping_factor = 1.0

    assert (
        sunlit_shaded_leaves.calc_direct_extinction_coefficient(
            solar_inclination,
            leaf_scattering_coefficient,
            leaf_angle_distribution_factor,
            clumping_factor,
        )
        == 0.0
    )


def test_calc_direct_extinction_coefficient_returns_expected_value():
    leaf_scattering_coefficient = 0.15
    solar_inclination = pi / 2.0
    expected_value = 0.46260740831950214
    leaf_angle_distribution_factor = 0.9773843811168246
    clumping_factor = 1.0

    actual_value = sunlit_shaded_leaves.calc_direct_extinction_coefficient(
        solar_inclination,
        leaf_scattering_coefficient,
        leaf_angle_distribution_factor,
        clumping_factor,
    )

    testing.assert_almost_equal(actual_value, expected_value, decimal=6)


def test_calc_sky_sectors_weight_returns_expected_uoc_values():
    assert sunlit_shaded_leaves.calc_sky_sectors_weight(3, "uoc") == [0.25, 0.5, 0.25]


def test_calc_sky_sectors_weight_returns_expected_soc_values():
    actual_values = sunlit_shaded_leaves.calc_sky_sectors_weight(3, "soc")
    expected_values = [0.1785714285714285, 0.5140108873361879, 0.3074176840923834]

    testing.assert_almost_equal(actual_values, expected_values, decimal=6)


def test_calc_sky_sectors_weight_returns_empty_list_for_unknown_sky_type():
    assert (
        sunlit_shaded_leaves.calc_sky_sectors_weight(3, "some unkonwn sky type") == []
    )


def test_calc_sky_sectors_weight_returns_weights_which_sums_up_to_1():
    for sky_type in ("soc", "uoc"):
        actual_value = sum(sunlit_shaded_leaves.calc_sky_sectors_weight(3, sky_type))
        expected_value = 1.0

        testing.assert_almost_equal(actual_value, expected_value, decimal=6)


def test_calc_diffuse_extinction_coefficient_reduces_as_leaf_area_index_increases():
    leaf_scattering_coefficient = 0.15
    leaf_angle_distribution_factor = 0.9773843811168246
    clumping_factor = 1

    diffuse_coeffcients = [
        sunlit_shaded_leaves.calc_diffuse_extinction_coefficient(
            leaf_area_index=leaf_area_index,
            leaf_scattering_coefficient=leaf_scattering_coefficient,
            leaf_angle_distribution_factor=leaf_angle_distribution_factor,
            clumping_factor=clumping_factor,
        )
        for leaf_area_index in arange(0, 5.1, 0.1)
    ]

    assert_values_trend(values=diffuse_coeffcients, trend="decreasing")


def test_calc_diffuse_extinction_coefficient_returns_greater_extinction_coefficient_for_black_leaves():
    leaf_area_index = 3.0
    leaf_scattering_coefficient = 0.15
    sky_sectors_number = 3
    leaf_angle_distribution_factor = 0.9773843811168246
    clumping_factor = 1

    for sky_type in ("soc", "uoc"):
        extinction_coef, black_extinction_coef = (
            sunlit_shaded_leaves.calc_diffuse_extinction_coefficient(
                leaf_area_index=leaf_area_index,
                leaf_angle_distribution_factor=leaf_angle_distribution_factor,
                clumping_factor=clumping_factor,
                leaf_scattering_coefficient=leaf_scattering_coefficient,
                sky_sectors_number=sky_sectors_number,
                sky_type=sky_type,
            )
        )

    assert extinction_coef < black_extinction_coef


def test_calc_diffuse_extinction_coefficient_returns_expected_values():
    leaf_area_index = 3.0
    leaf_scattering_coefficient = 0.15
    sky_sectors_number = 3
    leaf_angle_distribution_factor = 0.9773843811168246
    clumping_factor = 1

    expected_values = {
        "soc": (0.6390947959070368, 0.6872841045179627),
        "uoc": (0.675874154734713, 0.7250108165502616),
    }

    for sky_type in ("soc", "uoc"):
        actual_values = sunlit_shaded_leaves.calc_diffuse_extinction_coefficient(
            leaf_area_index=leaf_area_index,
            leaf_angle_distribution_factor=leaf_angle_distribution_factor,
            clumping_factor=clumping_factor,
            leaf_scattering_coefficient=leaf_scattering_coefficient,
            sky_sectors_number=sky_sectors_number,
            sky_type=sky_type,
        )

    testing.assert_almost_equal(actual_values, expected_values[sky_type], decimal=3)


def test_calc_canopy_reflectance_to_direct_irradiance_is_zero_when_leaf_scattering_is_zero():
    assert (
        sunlit_shaded_leaves.calc_canopy_reflectance_to_direct_irradiance(
            random.rand(), 0.0
        )
        == 0.0
    )


def test_calc_canopy_reflectance_to_direct_irradiance_increases_as_leaf_scattering_increases():
    canopy_reflectance = [
        sunlit_shaded_leaves.calc_canopy_reflectance_to_direct_irradiance(
            0.5, scattering_coef
        )
        for scattering_coef in arange(0, 1.1, 0.1)
    ]

    assert_values_trend(values=canopy_reflectance, trend="increasing")


def test_calc_canopy_reflectance_to_direct_irradiance_increases_as_direct_black_extinction_coefficient_increases():
    canopy_reflectance = [
        sunlit_shaded_leaves.calc_canopy_reflectance_to_direct_irradiance(
            extinction_coef, 0.15
        )
        for extinction_coef in arange(0, 1.1, 0.1)
    ]

    assert_values_trend(values=canopy_reflectance, trend="increasing")


def test_calc_sunlit_fraction_is_bounded_by_zero_and_unity():
    sunlit_fraction = [
        sunlit_shaded_leaves.calc_sunlit_fraction(cumulative_leaf_area_index, 0.5)
        for cumulative_leaf_area_index in arange(0, 5, 0.1)
    ]

    assert all([0 <= x <= 1 for x in sunlit_fraction])


def test_calc_sunlit_fraction_decreases_as_cumulative_leaf_area_index_increases():
    sunlit_fraction = [
        sunlit_shaded_leaves.calc_sunlit_fraction(cumulative_leaf_area_index, 0.5)
        for cumulative_leaf_area_index in arange(0, 5, 0.1)
    ]

    assert_values_trend(values=sunlit_fraction, trend="decreasing")


def test_calc_sunlit_fraction_decreases_as_extinction_coefficient_increases():
    sunlit_fraction = [
        sunlit_shaded_leaves.calc_sunlit_fraction(3.0, extinction_coef)
        for extinction_coef in arange(0.5, 10.5, 0.5)
    ]

    assert_values_trend(values=sunlit_fraction, trend="decreasing")


def test_calc_shaded_fraction_is_bounded_by_zero_and_unity():
    shaded_fraction = [
        sunlit_shaded_leaves.calc_shaded_fraction(cumulative_leaf_area_index, 0.5)
        for cumulative_leaf_area_index in arange(0, 5, 0.1)
    ]

    assert all([0 <= x <= 1 for x in shaded_fraction])


def test_calc_shaded_fraction_increases_as_cumulative_leaf_area_index_increases():
    shaded_fraction = [
        sunlit_shaded_leaves.calc_shaded_fraction(cumulative_leaf_area_index, 0.5)
        for cumulative_leaf_area_index in arange(0, 5, 0.1)
    ]

    assert_values_trend(values=shaded_fraction, trend="increasing")


def test_calc_shaded_fraction_increases_as_direct_black_extinction_coefficient_increases():
    shaded_fraction = [
        sunlit_shaded_leaves.calc_shaded_fraction(3.0, extinction_coef)
        for extinction_coef in arange(0.5, 10.5, 0.5)
    ]

    assert_values_trend(values=shaded_fraction, trend="increasing")


def test_sunlit_and_shaded_fractions_sum_up_to_1():
    sunlit_fraction, shaded_fraction = zip(
        *[
            (
                sunlit_shaded_leaves.calc_sunlit_fraction(
                    cumulative_leaf_area_index, 0.5
                ),
                sunlit_shaded_leaves.calc_shaded_fraction(
                    cumulative_leaf_area_index, 0.5
                ),
            )
            for cumulative_leaf_area_index in arange(0, 5, 0.1)
        ]
    )

    actual_values = [x + y for x, y in zip(sunlit_fraction, shaded_fraction)]

    testing.assert_almost_equal(actual_values, 1, decimal=1)


def test_calc_absorbed_direct_irradiance_is_positive():
    absorbed_irradiance = [
        sunlit_shaded_leaves.calc_absorbed_direct_irradiance(
            incident_direct_irradiance, 0.15, 0.5
        )
        for incident_direct_irradiance in range(0, 800, 100)
    ]

    assert all([x >= 0 for x in absorbed_irradiance])


def test_calc_absorbed_direct_irradiance_increases_as_incident_direct_irradiance_increases():
    absorbed_irradiance = [
        sunlit_shaded_leaves.calc_absorbed_direct_irradiance(
            incident_direct_irradiance, 0.15, 0.5
        )
        for incident_direct_irradiance in range(0, 800, 100)
    ]

    assert_values_trend(values=absorbed_irradiance, trend="increasing")


def test_calc_absorbed_direct_irradiance_decreases_as_leaf_scattering_coefficient_decreases():
    absorbed_irradiance = [
        sunlit_shaded_leaves.calc_absorbed_direct_irradiance(
            800.0, leaf_scattering, 0.5
        )
        for leaf_scattering in arange(0, 1.1, 0.1)
    ]

    assert_values_trend(values=absorbed_irradiance, trend="decreasing")


def test_calc_absorbed_direct_irradiance_increases_as_direct_black_extinction_coefficient_increases():
    absorbed_irradiance = [
        sunlit_shaded_leaves.calc_absorbed_direct_irradiance(
            800.0, 0.15, extinction_coef
        )
        for extinction_coef in arange(0.5, 10.5, 0.5)
    ]

    assert_values_trend(values=absorbed_irradiance, trend="increasing")


def test_calc_absorbed_diffuse_irradiance_at_given_depth_is_positive():
    absorbed_irradiance = [
        sunlit_shaded_leaves.calc_absorbed_diffuse_irradiance_at_given_depth(
            incident_diffuse_irradiance, 3.0, 0.4, 0.64
        )
        for incident_diffuse_irradiance in range(0, 80, 10)
    ]

    assert all([x >= 0 for x in absorbed_irradiance])


def test_calc_absorbed_diffuse_irradiance_at_given_depth_increases_as_incident_diffuse_irradiance_increases():
    absorbed_irradiance = [
        sunlit_shaded_leaves.calc_absorbed_diffuse_irradiance_at_given_depth(
            incident_diffuse_irradiance, 3.0, 0.4, 0.64
        )
        for incident_diffuse_irradiance in range(0, 80, 10)
    ]

    assert_values_trend(values=absorbed_irradiance, trend="increasing")


def test_calc_absorbed_diffuse_irradiance_at_given_depth_decreases_as_cumulative_leaf_area_index_increases():
    absorbed_irradiance = [
        sunlit_shaded_leaves.calc_absorbed_diffuse_irradiance_at_given_depth(
            10.0, cumulative_leaf_area_index, 0.4, 0.64
        )
        for cumulative_leaf_area_index in arange(0, 5, 0.1)
    ]

    assert_values_trend(values=absorbed_irradiance, trend="decreasing")


def test_calc_absorbed_diffuse_irradiance_at_given_depth_decreases_as_canopy_reflectance_increases():
    absorbed_irradiance = [
        sunlit_shaded_leaves.calc_absorbed_diffuse_irradiance_at_given_depth(
            10.0, 3.0, canopy_reflectance, 0.64
        )
        for canopy_reflectance in arange(0, 1.1, 0.1)
    ]

    assert_values_trend(values=absorbed_irradiance, trend="decreasing")


def test_calc_absorbed_diffuse_irradiance_at_given_depth_does_not_have_monotonic_trend_with_diffuse_extinction_coef():
    absorbed_irradiance = [
        sunlit_shaded_leaves.calc_absorbed_diffuse_irradiance_at_given_depth(
            10.0, 3.0, 0.4, diffuse_extinction_coefficient
        )
        for diffuse_extinction_coefficient in arange(0, 1.1, 0.1)
    ]

    assert_values_trend(values=absorbed_irradiance, trend="non-monotonic")


def test_calc_absorbed_diffuse_irradiance_at_given_depth_peaks_at_predefined_value():
    absorbed_irradiance = [
        sunlit_shaded_leaves.calc_absorbed_diffuse_irradiance_at_given_depth(
            10.0, 3.0, 0.4, diffuse_extinction_coefficient
        )
        for diffuse_extinction_coefficient in arange(0, 1.1, 0.1)
    ]
    absorbed_irradiance_max = absorbed_irradiance[3]

    assert all(
        [
            abs_irradiance <= absorbed_irradiance_max
            for abs_irradiance in absorbed_irradiance
        ]
    )


def test_calc_absorbed_scattered_irradiance_at_given_depth_is_positive():
    upper_cumulative_leaf_area_index = 1.0
    direct_extinction_coefficient = 0.46
    direct_black_extinction_coefficient = 0.5
    canopy_reflectance_to_direct_irradiance = 0.027
    leaf_scattering_coefficient = 0.15

    absorbed_irradiance = [
        sunlit_shaded_leaves.calc_absorbed_scattered_irradiance_at_given_depth(
            incident_direct_irradiance,
            upper_cumulative_leaf_area_index,
            direct_extinction_coefficient,
            direct_black_extinction_coefficient,
            canopy_reflectance_to_direct_irradiance,
            leaf_scattering_coefficient,
        )
        for incident_direct_irradiance in range(100, 800, 100)
    ]

    assert all([x >= 0 for x in absorbed_irradiance])


def test_calc_absorbed_scattered_irradiance_at_given_depth_increases_as_incident_irradiance_increases():
    upper_cumulative_leaf_area_index = 1.0
    direct_extinction_coefficient = 0.46
    direct_black_extinction_coefficient = 0.5
    canopy_reflectance_to_direct_irradiance = 0.027
    leaf_scattering_coefficient = 0.15

    absorbed_irradiance = [
        sunlit_shaded_leaves.calc_absorbed_scattered_irradiance_at_given_depth(
            incident_direct_irradiance,
            upper_cumulative_leaf_area_index,
            direct_extinction_coefficient,
            direct_black_extinction_coefficient,
            canopy_reflectance_to_direct_irradiance,
            leaf_scattering_coefficient,
        )
        for incident_direct_irradiance in range(100, 800, 100)
    ]

    assert_values_trend(values=absorbed_irradiance, trend="increasing")


def test_calc_absorbed_scattered_irradiance_at_given_depth_does_not_have_monotonic_trend_with_leaf_area_index():
    incident_direct_irradiance = 500.0
    direct_extinction_coefficient = 0.46
    direct_black_extinction_coefficient = 0.5
    canopy_reflectance_to_direct_irradiance = 0.027
    leaf_scattering_coefficient = 0.15

    absorbed_irradiance = [
        sunlit_shaded_leaves.calc_absorbed_scattered_irradiance_at_given_depth(
            incident_direct_irradiance,
            upper_cumulative_leaf_area_index,
            direct_extinction_coefficient,
            direct_black_extinction_coefficient,
            canopy_reflectance_to_direct_irradiance,
            leaf_scattering_coefficient,
        )
        for upper_cumulative_leaf_area_index in arange(0, 5, 0.1)
    ]

    assert_values_trend(values=absorbed_irradiance, trend="non-monotonic")


def test_calc_absorbed_scattered_irradiance_at_given_depth_increases_as_direct_extinction_coefficients_increase():
    incident_direct_irradiance = 500.0
    upper_cumulative_leaf_area_index = 1.0
    canopy_reflectance_to_direct_irradiance = 0.027
    leaf_scattering_coefficient = 0.15

    absorbed_irradiance = [
        sunlit_shaded_leaves.calc_absorbed_scattered_irradiance_at_given_depth(
            incident_direct_irradiance,
            upper_cumulative_leaf_area_index,
            direct_extinction_coefficient,
            direct_black_extinction_coefficient,
            canopy_reflectance_to_direct_irradiance,
            leaf_scattering_coefficient,
        )
        for direct_extinction_coefficient, direct_black_extinction_coefficient in zip(
            [0.461, 0.532, 0.922], [0.5, 0.577, 1]
        )
    ]

    assert_values_trend(values=absorbed_irradiance, trend="increasing")


def test_calc_absorbed_scattered_irradiance_at_given_depth_decreases_as_canopy_reflectance_increases():
    incident_direct_irradiance = 500.0
    upper_cumulative_leaf_area_index = 1.0
    direct_extinction_coefficient = 0.46
    direct_black_extinction_coefficient = 0.5
    leaf_scattering_coefficient = 0.15

    absorbed_irradiance = [
        sunlit_shaded_leaves.calc_absorbed_scattered_irradiance_at_given_depth(
            incident_direct_irradiance,
            upper_cumulative_leaf_area_index,
            direct_extinction_coefficient,
            direct_black_extinction_coefficient,
            canopy_reflectance_to_direct_irradiance,
            leaf_scattering_coefficient,
        )
        for canopy_reflectance_to_direct_irradiance in arange(0, 0.05, 0.01)
    ]

    assert_values_trend(values=absorbed_irradiance, trend="decreasing")


def test_calc_absorbed_scattered_irradiance_at_given_depth_increases_as_leaf_scattering_increases():
    incident_direct_irradiance = 500.0
    upper_cumulative_leaf_area_index = 1.0
    direct_extinction_coefficient = 0.46
    direct_black_extinction_coefficient = 0.5
    canopy_reflectance_to_direct_irradiance = 0.027

    absorbed_irradiance = [
        sunlit_shaded_leaves.calc_absorbed_scattered_irradiance_at_given_depth(
            incident_direct_irradiance,
            upper_cumulative_leaf_area_index,
            direct_extinction_coefficient,
            direct_black_extinction_coefficient,
            canopy_reflectance_to_direct_irradiance,
            leaf_scattering_coefficient,
        )
        for leaf_scattering_coefficient in arange(0, 1, 0.1)
    ]

    assert_values_trend(values=absorbed_irradiance, trend="increasing")


def test_calc_sunlit_fraction_per_leaf_layer_decreases_as_layer_thickness_increases():
    upper_cumulative_leaf_area_index = 3.0
    direct_black_extinction_coefficient = 0.5
    sunlit_fraction = [
        sunlit_shaded_leaves.calc_sunlit_fraction_per_leaf_layer(
            upper_cumulative_leaf_area_index,
            layer_thickness,
            direct_black_extinction_coefficient,
        )
        for layer_thickness in arange(0.1, 1, 0.1)
    ]

    assert_values_trend(values=sunlit_fraction, trend="decreasing")


def test_calc_absorbed_diffuse_irradiance_per_leaf_layer_is_positive():
    layer_thickness = 1.0
    upper_cumulative_leaf_area_index = 3.0
    canopy_reflectance_to_diffuse_irradiance = 0.057
    direct_black_extinction_coefficient = 0.5
    diffuse_extinction_coefficient = 0.64
    absorbed_irradiance = [
        sunlit_shaded_leaves.calc_absorbed_diffuse_irradiance_by_sunlit_leaf_layer(
            incident_diffuse_irradiance,
            upper_cumulative_leaf_area_index,
            layer_thickness,
            canopy_reflectance_to_diffuse_irradiance,
            direct_black_extinction_coefficient,
            diffuse_extinction_coefficient,
        )
        for incident_diffuse_irradiance in range(10, 100, 10)
    ]

    assert all([x >= 0 for x in absorbed_irradiance])


def test_calc_absorbed_diffuse_irradiance_per_leaf_layer_increases_as_layer_thickness_increases():
    incident_diffuse_irradiance = 10.0
    upper_cumulative_leaf_area_index = 3.0
    canopy_reflectance_to_diffuse_irradiance = 0.057
    direct_black_extinction_coefficient = 0.5
    diffuse_extinction_coefficient = 0.64
    absorbed_irradiance = [
        sunlit_shaded_leaves.calc_absorbed_diffuse_irradiance_by_sunlit_leaf_layer(
            incident_diffuse_irradiance,
            upper_cumulative_leaf_area_index,
            layer_thickness,
            canopy_reflectance_to_diffuse_irradiance,
            direct_black_extinction_coefficient,
            diffuse_extinction_coefficient,
        )
        for layer_thickness in arange(0.1, 1, 0.1)
    ]

    assert_values_trend(values=absorbed_irradiance, trend="increasing")


def test_calc_absorbed_scattered_irradiance_per_leaf_layer_increases_as_leaf_layer_thickness_increases():
    incident_direct_irradiance = 500.0
    upper_cumulative_leaf_area_index = 1.0
    direct_extinction_coefficient = 0.46
    direct_black_extinction_coefficient = 0.5
    canopy_reflectance_to_direct_irradiance = 0.027
    leaf_scattering_coefficient = 0.15

    absorbed_irradiance = [
        sunlit_shaded_leaves.calc_absorbed_scattered_irradiance_by_sunlit_leaf_layer(
            incident_direct_irradiance,
            upper_cumulative_leaf_area_index,
            leaf_layer_thickness,
            direct_extinction_coefficient,
            direct_black_extinction_coefficient,
            canopy_reflectance_to_direct_irradiance,
            leaf_scattering_coefficient,
        )
        for leaf_layer_thickness in arange(0.1, 3, 0.1)
    ]

    assert_values_trend(values=absorbed_irradiance, trend="increasing")
