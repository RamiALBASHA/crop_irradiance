from math import radians

import matplotlib.pyplot as plt
from crop_irradiance.uniform_crops import inputs, params, shoot


def generate_plots(incident_direct_irradiance: float, incident_diffuse_irradiance: float,
                   lumped_canopy: shoot.Shoot, sunlit_shaded_canopy: shoot.Shoot):
    layer_indexes, lumped_layer_irradiance = zip(
        *[(index, layer.absorbed_irradiance['lumped']) for index, layer in lumped_canopy.items()])
    _, sunlit_layer_irradiance, shaded_layer_irradiance = zip(
        *[(index, layer.absorbed_irradiance['sunlit'], layer.absorbed_irradiance['shaded'])
          for index, layer in sunlit_shaded_canopy.items()])

    assert layer_indexes == _

    plot_absorbed_irradiance_profiles(incident_diffuse_irradiance, incident_direct_irradiance, layer_indexes,
                                      lumped_layer_irradiance,
                                      shaded_layer_irradiance, sunlit_layer_irradiance)
    plot_linear_comparison(lumped_layer_irradiance, shaded_layer_irradiance, sunlit_layer_irradiance)


def plot_absorbed_irradiance_profiles(incident_diffuse_irradiance, incident_direct_irradiance, layer_indexes,
                                      lumped_layer_irradiance, shaded_layer_irradiance, sunlit_layer_irradiance):
    _, ax = plt.subplots()
    ax.vlines(incident_direct_irradiance,
              ymin=min(layer_indexes), ymax=max(layer_indexes), label='incident direct', color='y', linestyle='--')
    ax.vlines(incident_diffuse_irradiance,
              ymin=min(layer_indexes), ymax=max(layer_indexes), label='incident diffuse', color='r', linestyle='--')
    ax.plot(lumped_layer_irradiance, layer_indexes, label='lumped')
    ax.plot(sunlit_layer_irradiance, layer_indexes, label='sunlit')
    ax.plot(shaded_layer_irradiance, layer_indexes, label='shaded')
    ax.set(xlabel=r'$\mathregular{irradiance\/[W \cdot m^{-2}_{ground}]}$',
           xlim=(0, 1.01 * (incident_direct_irradiance + incident_diffuse_irradiance)),
           ylabel='layer index [-]', yticks=layer_indexes)
    ax.legend()
    plt.savefig('absorbed_irradiance_profile.png')
    plt.close()


def plot_linear_comparison(lumped_layer_irradiance, shaded_layer_irradiance, sunlit_layer_irradiance):
    _, ax = plt.subplots()
    ax.plot(lumped_layer_irradiance,
            [sum(abs_par) for abs_par in zip(sunlit_layer_irradiance, shaded_layer_irradiance)])
    ax.set(xlabel=r'$\mathregular{Lumped\/[W \cdot m^{-2}_{ground}]}$',
           ylabel=r'$\mathregular{Sunlit-shaded\/[W \cdot m^{-2}_{ground}]}$')
    ax.grid()
    plt.savefig('absorbed_irradiance_comparison.png')
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
    common_params = dict(leaf_reflectance=0.07, leaf_transmittance=0.0, leaves_to_sun_average_projection=0.5,
                         sky_sectors_number=3, sky_type='soc', canopy_reflectance_to_diffuse_irradiance=0.057)

    params_lumped = params.LumpedParams(model='de_pury', **common_params)
    params_sunlit_shaded = params.SunlitShadedParams(**common_params)

    hour = 12

    incident_direct_par = hourly_direct_par[hour]
    incident_diffuse_par = hourly_diffuse_par[hour]

    common_inputs = dict(
        leaf_layers={0: 1, 1: 1, 2: 1, 3: 1},
        incident_direct_irradiance=incident_direct_par,
        incident_diffuse_irradiance=incident_diffuse_par,
        solar_inclination=radians(solar_inclination[hour]))

    inputs_lumped = inputs.LumpedInputs(model='de_pury', **common_inputs)
    params_lumped.update(inputs_lumped)
    canopy_lumped = shoot.Shoot(leaves_category='lumped', inputs=inputs_lumped, params=params_lumped)
    canopy_lumped.calc_absorbed_irradiance()

    inputs_sunlit_shaded = inputs.SunlitShadedInputs(**common_inputs)
    params_sunlit_shaded.update(inputs_sunlit_shaded)
    canopy_sunlit_shaded = shoot.Shoot(leaves_category='sunlit-shaded', inputs=inputs_sunlit_shaded,
                                       params=params_sunlit_shaded)
    canopy_sunlit_shaded.calc_absorbed_irradiance()

    generate_plots(
        incident_direct_irradiance=incident_direct_par,
        incident_diffuse_irradiance=incident_diffuse_par,
        lumped_canopy=canopy_lumped,
        sunlit_shaded_canopy=canopy_sunlit_shaded)
