from math import radians
import matplotlib.pyplot as plt

from crop_irradiance.uniform_crops import inputs, params, shoot


def plot_comparison(abs_irradiance_lumped: list, abs_irradiance_sunlit_shaded: list):
    _, ax = plt.subplots()
    ax.plot(range(24), abs_irradiance_lumped, label='lumped')
    ax.plot(range(24), abs_irradiance_sunlit_shaded, label='sunlit_shaded')
    ax.legend()
    plt.savefig('absorbed_irradiance.png')
    plt.close()


hourly_direct_par = [0, 0, 0, 0, 0, 0, 0, 18.428820397314112, 86.779379638514726, 213.23527694182002,
                     332.53550250736947, 379.40012173450828, 359.77089500962774, 277.64770928541054,
                     133.08397549276251, 39.374833543598889, 1.1288678878776721, 0, 0, 0, 0, 0, 0, 0]

hourly_diffuse_par = [0, 0, 0, 0, 0, 0, 0, 18.428820397314112, 61.4976272200411, 74.918330146929719,
                      74.699625542626109, 85.077684125431659, 80.552408749094454, 65.365757925282779,
                      72.846107552867508, 37.432721347065836, 1.1288678878776721, 0, 0, 0, 0, 0, 0, 0]

solar_inclination = [-16.22, -16.22, -16.22, -15.39, -9.49, -1.91, 6.65, 15.92, 25.66, 35.47, 44.92, 53.28, 59.36,
                     61.44, 58.69, 52.18, 43.6, 34.06, 24.22, 14.51, 5.33, -3.2, -10.56, -16.22]

if __name__ == '__main__':

    params_lumped = params.LumpedParams(extinction_coefficient=0.5)
    sunlit_shaded_params = params.SunlitShadedParams(leaf_reflectance=0.07, leaf_transmittance=0.0,
                                                     leaves_to_sun_average_projection=0.5, sky_sectors_number=3,
                                                     sky_type='soc',
                                                     canopy_reflectance_to_diffuse_irradiance=0.057)

    abs_irradiance_lumped = []
    abs_irradiance_sunlit_shaded = []

    for hour in range(24):
        direct_par = hourly_direct_par[hour]
        diffuse_par = hourly_diffuse_par[hour]

        inputs_lumped = inputs.LumpedInputs(leaf_layers={0: 6.43}, incident_irradiance=direct_par + diffuse_par)
        canopy_lumped = shoot.Shoot(leaves_category='lumped', inputs=inputs_lumped, params=params_lumped)

        abs_irradiance_lumped.append([layer.absorbed_irradiance['lumped'] for layer in canopy_lumped.values()][0])

        sunlit_shaded_inputs = inputs.SunlitShadedInputs(leaf_layers={0: 6.43},
                                                         incident_direct_irradiance=direct_par,
                                                         incident_diffuse_irradiance=diffuse_par,
                                                         solar_inclination=radians(solar_inclination[hour]))

        sunlit_shaded_params.update(sunlit_shaded_inputs)

        sunlit_shaded_canopy = shoot.Shoot(leaves_category='sunlit-shaded', inputs=sunlit_shaded_inputs,
                                           params=sunlit_shaded_params)

        absorbed_sunlit_irradiance, absorbed_shaded_irradiance = zip(
            *[(layer.absorbed_irradiance['sunlit'], layer.absorbed_irradiance['shaded'])
              for index, layer in sunlit_shaded_canopy.items()])

        abs_irradiance_sunlit_shaded.append(absorbed_sunlit_irradiance[0] + absorbed_shaded_irradiance[0])

    plot_comparison(abs_irradiance_lumped, abs_irradiance_sunlit_shaded)
