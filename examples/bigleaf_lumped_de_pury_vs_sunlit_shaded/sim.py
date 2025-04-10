from math import radians

import matplotlib.pyplot as plt

from crop_irradiance.uniform_crops import inputs, params, shoot


def plot_comparison(
    abs_irradiance_lumped: list,
    abs_irradiance_sunlit: list,
    abs_irradiance_shaded: list,
):
    abs_irradiance_sunlit_shaded = [
        sum(x) for x in zip(abs_irradiance_sunlit, abs_irradiance_shaded)
    ]
    _, ax = plt.subplots()
    ax.plot(range(24), abs_irradiance_lumped, label="lumped")
    ax.plot(range(24), abs_irradiance_sunlit_shaded, label="sunlit_shaded")
    ax.legend()
    plt.savefig("absorbed_irradiance.png")
    plt.close()


def plot_absorbed_irradiance_separately(
    abs_irradiance_lumped: list,
    abs_irradiance_sunlit: list,
    abs_irradiance_shaded: list,
):
    hours = range(24)
    _, (ax_left, ax_right) = plt.subplots(
        ncols=2, sharey="all", sharex="all", figsize=(6.4, 2.4)
    )
    ax_left.plot(hours, abs_irradiance_lumped, label="lumped")
    ax_right.plot(hours, abs_irradiance_shaded, label="shaded")
    ax_right.plot(hours, abs_irradiance_sunlit, label="sunlit")

    for ax in (ax_left, ax_right):
        ax.legend()
        ax.set_xlabel("hours")
    ax_left.set_ylabel(
        "$\mathregular{absorbed\/irradiance\/[W \cdot m^{-2}_{ground}]}$"
    )
    plt.tight_layout()
    plt.savefig("absorbed_irradiance2.png")
    plt.close()


def plot_leaf_fractions_separately(sunlit: list, shaded: list):
    hours = range(24)
    _, (ax_left, ax_right) = plt.subplots(
        ncols=2, sharey="all", sharex="all", figsize=(6.4, 2.4)
    )
    ax_left.plot(hours, [1] * 24, label="lumped")
    ax_right.plot(hours, shaded, label="shaded")
    ax_right.plot(hours, sunlit, label="sunlit")

    for ax in (ax_left, ax_right):
        ax.legend()
        ax.set_xlabel("hours")
    ax_left.set_ylabel(
        "$\mathregular{leaf\/fraction\/[m^{2}_{leaf} \cdot m^{-2}_{ground}]}$"
    )
    plt.tight_layout()
    plt.savefig("leaf_fractions.png")
    plt.close()


hourly_direct_par = [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    18.428820397314112,
    86.779379638514726,
    213.23527694182002,
    332.53550250736947,
    379.40012173450828,
    359.77089500962774,
    277.64770928541054,
    133.08397549276251,
    39.374833543598889,
    1.1288678878776721,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
]

hourly_diffuse_par = [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    18.428820397314112,
    61.4976272200411,
    74.918330146929719,
    74.699625542626109,
    85.077684125431659,
    80.552408749094454,
    65.365757925282779,
    72.846107552867508,
    37.432721347065836,
    1.1288678878776721,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
]

solar_inclination = [
    -16.22,
    -16.22,
    -16.22,
    -15.39,
    -9.49,
    -1.91,
    6.65,
    15.92,
    25.66,
    35.47,
    44.92,
    53.28,
    59.36,
    61.44,
    58.69,
    52.18,
    43.6,
    34.06,
    24.22,
    14.51,
    5.33,
    -3.2,
    -10.56,
    -16.22,
]

if __name__ == "__main__":

    params_lumped = params.LumpedParams(
        model="de_pury",
        leaf_reflectance=0.07,
        leaf_transmittance=0.0,
        leaves_to_sun_average_projection=0.9773843811168246,
        sky_sectors_number=3,
        sky_type="soc",
        canopy_reflectance_to_diffuse_irradiance=0.057,
    )
    params_sunlit_shaded = params.SunlitShadedParams(
        leaf_reflectance=0.07,
        leaf_transmittance=0.0,
        leaf_angle_distribution_factor=0.9773843811168246,
        sky_sectors_number=3,
        sky_type="soc",
        canopy_reflectance_to_diffuse_irradiance=0.057,
    )

    abs_irradiance_lumped = []
    abs_irradiance_sunlit = []
    abs_irradiance_shaded = []
    fraction_sunlit = []
    fraction_shaded = []

    for hour in range(24):
        direct_par = hourly_direct_par[hour]
        diffuse_par = hourly_diffuse_par[hour]

        inputs_lumped = inputs.LumpedInputs(
            model="de_pury",
            leaf_layers={0: 6.43},
            incident_direct_irradiance=direct_par,
            incident_diffuse_irradiance=diffuse_par,
            solar_inclination=radians(solar_inclination[hour]),
        )

        params_lumped.update(inputs_lumped)

        canopy_lumped = shoot.Shoot(
            leaves_category="lumped", inputs=inputs_lumped, params=params_lumped
        )
        canopy_lumped.calc_absorbed_irradiance()

        abs_irradiance_lumped.append(
            [layer.absorbed_irradiance["lumped"] for layer in canopy_lumped.values()]
        )

        inputs_sunlit_shaded = inputs.SunlitShadedInputs(
            leaf_layers={0: 6.43},
            incident_direct_irradiance=direct_par,
            incident_diffuse_irradiance=diffuse_par,
            solar_inclination=radians(solar_inclination[hour]),
        )

        params_sunlit_shaded.update(inputs_sunlit_shaded)

        canopy_sunlit_shaded = shoot.Shoot(
            leaves_category="sunlit-shaded",
            inputs=inputs_sunlit_shaded,
            params=params_sunlit_shaded,
        )
        canopy_sunlit_shaded.calc_absorbed_irradiance()

        absorbed_sunlit_irradiance, absorbed_shaded_irradiance = zip(
            *[
                (
                    layer.absorbed_irradiance["sunlit"],
                    layer.absorbed_irradiance["shaded"],
                )
                for index, layer in canopy_sunlit_shaded.items()
            ]
        )

        abs_irradiance_sunlit.append(absorbed_sunlit_irradiance[0])
        abs_irradiance_shaded.append(absorbed_shaded_irradiance[0])
        fraction_sunlit.append(canopy_sunlit_shaded[0].sunlit_fraction)
        fraction_shaded.append(canopy_sunlit_shaded[0].shaded_fraction)

    plot_comparison(abs_irradiance_lumped, abs_irradiance_sunlit, abs_irradiance_shaded)
    plot_absorbed_irradiance_separately(
        abs_irradiance_lumped, abs_irradiance_sunlit, abs_irradiance_shaded
    )
    plot_leaf_fractions_separately(fraction_sunlit, fraction_shaded)
