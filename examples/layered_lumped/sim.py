from crop_irradiance.uniform_crops import inputs, params, shoot
from matplotlib import pyplot as plt

leaf_layers = {4: 0.09,
               5: 1.11,
               6: 1.92,
               7: 3.22}

sim_inputs = inputs.LumpedInputs(leaf_layers=leaf_layers, incident_irradiance=440)
sim_params = params.LumpedParams(extinction_coefficient=0.5)
canopy = shoot.Shoot(leaves_category='lumped', inputs=sim_inputs, params=sim_params)
canopy.calc_absorbed_irradiance()

layer_index, absorbed_irradiance = zip(
    *[(index, layer.absorbed_irradiance['lumped']) for index, layer in canopy.items()])

_, ax = plt.subplots()
ax.vlines(sim_inputs.incident_irradiance, ymin=min(leaf_layers.keys()), ymax=max(leaf_layers.keys()), label='incident')
ax.plot(absorbed_irradiance, layer_index, 'yo-', label='absorbed')
ax.set(xlabel='$\mathregular{irradiance\/[W \cdot m^{-2}_{ground}]}$', xlim=(0, 1.01 * sim_inputs.incident_irradiance),
       ylabel='layer index [-]', yticks=layer_index)
ax.legend()
plt.savefig(f'absorbed_irradiance.png')
plt.close()
