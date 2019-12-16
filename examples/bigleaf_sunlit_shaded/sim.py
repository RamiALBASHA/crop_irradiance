from math import pi

from crop_irradiance.uniform_crops import inputs, params, shoot
from matplotlib import pyplot as plt


sim_inputs = inputs.SunlitShadedInputs(leaf_layers={0: 6.43}, incident_direct_irradiance=500,
                                       incident_diffuse_irradiance=100, solar_inclination=pi / 3)

sim_params = params.SunlitShadedParams(leaf_reflectance=0.08, leaf_transmittance=0.07,
                                       leaves_to_sun_average_projection=0.5, sky_sectors_number=3, sky_type='soc',
                                       canopy_reflectance_to_diffuse_irradiance=0.057)
sim_params.update(sim_inputs)

canopy = shoot.Shoot(leaves_category='sunlit-shaded', inputs=sim_inputs, params=sim_params)

layer_index, absorbed_sunlit_irradiance, absorbed_shaded_irradiance = zip(
    *[(index, layer.absorbed_irradiance['sunlit'], layer.absorbed_irradiance['shaded'])
      for index, layer in canopy.items()])

_, ax = plt.subplots()
ax.plot(sim_inputs.incident_direct_irradiance, 0, 'yO', label='incident sunlit')
ax.plot(sim_inputs.incident_diffuse_irradiance, 0, 'rO', label='incident sunlit')
ax.plot(absorbed_sunlit_irradiance, layer_index, 'yo', label='absorbed sunlit')
ax.plot(absorbed_shaded_irradiance, layer_index, 'ro-', label='absorbed shaded')
ax.set(xlabel='$\mathregular{irradiance\/[W \cdot m^{-2}_{ground}]}$',
       xlim=(0, 1.01 * max(sim_inputs.incident_direct_irradiance, sim_inputs.incident_diffuse_irradiance)),
       ylabel='layer index [-]', yticks=layer_index)
ax.legend()
plt.savefig(f'absorbed_irradiance.png')
plt.close()
