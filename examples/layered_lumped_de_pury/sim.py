from math import pi

from crop_irradiance.uniform_crops import inputs, params, shoot
from matplotlib import pyplot as plt

leaf_layers = {4: 0.09,
               5: 1.11,
               6: 1.92,
               7: 3.22}

sim_inputs = inputs.LumpedInputs(model='de_pury',
                                 leaf_layers=leaf_layers, incident_direct_irradiance=360,
                                 incident_diffuse_irradiance=80, solar_inclination=pi / 3)

sim_params = params.LumpedParams(model='de_pury',
                                 leaf_reflectance=0.08, leaf_transmittance=0.07,
                                 leaves_to_sun_average_projection=0.9773843811168246,
                                 sky_sectors_number=3, sky_type='soc',
                                 canopy_reflectance_to_diffuse_irradiance=0.057)
sim_params.update(sim_inputs)

canopy = shoot.Shoot(leaves_category='lumped', inputs=sim_inputs, params=sim_params)
canopy.calc_absorbed_irradiance()

layer_index, absorbed_irradiance = zip(*[(index, layer.absorbed_irradiance['lumped'])
                                         for index, layer in canopy.items()])

_, ax = plt.subplots()
ax.vlines(sim_inputs.incident_direct_irradiance,
          ymin=min(leaf_layers.keys()), ymax=max(leaf_layers.keys()), label='incident direct', color='y')
ax.vlines(sim_inputs.incident_diffuse_irradiance,
          ymin=min(leaf_layers.keys()), ymax=max(leaf_layers.keys()), label='incident diffuse', color='r')
ax.plot(absorbed_irradiance, layer_index, 'yo-', label='absorbed lumped')
ax.set(xlabel='$\mathregular{irradiance\/[W \cdot m^{-2}_{ground}]}$',
       xlim=(0, 1.01 * max(sim_inputs.incident_direct_irradiance, sim_inputs.incident_diffuse_irradiance)),
       ylabel='layer index [-]', yticks=layer_index)
ax.legend()
plt.savefig('absorbed_irradiance.png')
plt.close()
