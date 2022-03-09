from math import pi

from crop_irradiance.uniform_crops import inputs, params, shoot
from matplotlib import pyplot as plt

leaf_layers = {0: 6.43}

sim_inputs = inputs.SunlitShadedInputs(leaf_layers={0: 6.43}, incident_direct_irradiance=360,
                                       incident_diffuse_irradiance=80, solar_inclination=pi / 3)

sim_params = params.SunlitShadedParams(leaf_reflectance=0.08, leaf_transmittance=0.07,
                                       leaf_angle_distribution_factor=0.9773843811168246,
                                       sky_sectors_number=3, sky_type='soc',
                                       canopy_reflectance_to_diffuse_irradiance=0.057)
sim_params.update(sim_inputs)

canopy = shoot.Shoot(leaves_category='sunlit-shaded', inputs=sim_inputs, params=sim_params)
canopy.calc_absorbed_irradiance()

layer_index, absorbed_sunlit_irradiance, absorbed_shaded_irradiance = zip(
    *[(index, layer.absorbed_irradiance['sunlit'], layer.absorbed_irradiance['shaded'])
      for index, layer in canopy.items()])

_, ax = plt.subplots()
ax.vlines(sim_inputs.incident_direct_irradiance,
          ymin=-0.02, ymax=0.02, label='incident direct', color='y')
ax.vlines(sim_inputs.incident_diffuse_irradiance,
          ymin=-0.02, ymax=0.02, label='incident diffuse', color='r')
ax.plot(absorbed_sunlit_irradiance, layer_index, 'yo-', label='absorbed sunlit')
ax.plot(absorbed_shaded_irradiance, layer_index, 'ro-', label='absorbed shaded')
ax.set(xlabel=r'$\mathregular{irradiance\/[W \cdot m^{-2}_{ground}]}$',
       ylabel='layer index [-]', yticks=layer_index)
ax.legend()
plt.savefig('absorbed_irradiance.png')
plt.close()
