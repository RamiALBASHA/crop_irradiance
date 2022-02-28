from math import pi

from crop_irradiance.uniform_crops import inputs, params, shoot
from matplotlib import pyplot as plt


def set_shoot() -> shoot.Shoot:
    leaf_layers = {k: 1 for k in range(8)}

    sim_inputs = inputs.SunlitShadedInputs(
        leaf_layers=leaf_layers,
        incident_direct_irradiance=360,
        incident_diffuse_irradiance=80,
        solar_inclination=pi / 3)

    sim_params = params.SunlitShadedParams(leaf_reflectance=0.08, leaf_transmittance=0.07,
                                           leaf_angle_distribution_factor=0.9773843811168246,
                                           sky_sectors_number=3, sky_type='soc',
                                           canopy_reflectance_to_diffuse_irradiance=0.057)
    sim_params.update(sim_inputs)

    canopy = shoot.Shoot(leaves_category='sunlit-shaded', inputs=sim_inputs, params=sim_params)
    canopy.calc_absorbed_irradiance()

    return canopy


def plot_results(canopy: shoot.Shoot):
    sunlit_fraction = []
    sunlit_beam = []
    sunlit_diffuse = []
    sunlit_scattered = []
    shaded_diffuse = []
    shaded_scattered = []
    layer_indexes = list(canopy.keys())
    for index in layer_indexes:
        sunlit_fraction.append(canopy[index].sunlit_fraction)
        sunlit_beam.append(
            (canopy[index].abs_direct_by_sunlit, canopy[index].thickness * canopy[index].sunlit_fraction))
        sunlit_diffuse.append(
            (canopy[index].abs_diffuse_by_sunlit, canopy[index].thickness * canopy[index].sunlit_fraction))
        sunlit_scattered.append(
            (canopy[index].abs_scattered_by_sunlit, canopy[index].thickness * canopy[index].sunlit_fraction))
        shaded_diffuse.append(
            (canopy[index].abs_diffuse_by_shaded, canopy[index].thickness * canopy[index].shaded_fraction))
        shaded_scattered.append(
            (canopy[index].abs_scattered_by_shaded, canopy[index].thickness * canopy[index].shaded_fraction))

    fig, axs = plt.subplots(ncols=3, nrows=2)
    axs[0, 0].fill_between(sunlit_fraction, layer_indexes, y2=7, color='yellow')
    axs[0, 0].fill_between(sunlit_fraction, layer_indexes, y2=0, color='orange')
    axs[0, 0].fill_between([max(sunlit_fraction), 1], [0, 0], y2=7, color='orange')
    axs[0, 0].set(xlim=(0, 1), xlabel='fraction [-]', ylim=(0, 7), yticks=range(8), ylabel='layer index [-]')
    [fig.delaxes(ax) for ax in list(axs[0, 1:]) + list(axs[1, :])]
    axs[0, 0].text(0.075, 0.85, 'sunlit', transform=axs[0, 0].transAxes)
    axs[0, 0].text(0.5, 0.35, 'shaded', transform=axs[0, 0].transAxes)
    fig.tight_layout()
    plt.savefig('fractions.png')

    fig2, axs = plt.subplots(ncols=3, nrows=2, sharex='col', sharey='all')

    axs[0, 0].plot([v[0] for v in sunlit_beam], layer_indexes, label=r'$\mathregular{W\/m^{-2}_{ground}}$')
    axs[0, 0].plot([v[0] / v[1] for v in sunlit_beam], layer_indexes, label=r'$\mathregular{W\/m^{-2}_{leaf}}$')

    axs[0, 1].plot([v[0] for v in sunlit_diffuse], layer_indexes, label=r'$\mathregular{W\/m^{-2}_{ground}}$')
    axs[0, 1].plot([v[0] / v[1] for v in sunlit_diffuse], layer_indexes, label=r'$\mathregular{W\/m^{-2}_{leaf}}$')

    axs[0, 2].plot([v[0] for v in sunlit_scattered], layer_indexes, label=r'$\mathregular{W\/m^{-2}_{ground}}$')
    axs[0, 2].plot([v[0] / v[1] for v in sunlit_scattered], layer_indexes, label=r'$\mathregular{W\/m^{-2}_{leaf}}$')

    axs[1, 1].plot([v[0] for v in shaded_diffuse], layer_indexes, label=r'$\mathregular{W\/m^{-2}_{ground}}$')
    axs[1, 1].plot([v[0] / v[1] for v in shaded_diffuse], layer_indexes, label=r'$\mathregular{W\/m^{-2}_{leaf}}$')

    axs[1, 2].plot([v[0] for v in shaded_scattered], layer_indexes, label=r'$\mathregular{W\/m^{-2}_{ground}}$')
    axs[1, 2].plot([v[0] / v[1] for v in shaded_scattered], layer_indexes, label=r'$\mathregular{W\/m^{-2}_{leaf}}$')

    fig2.delaxes(axs[1, 0])

    axs[0, 0].xaxis.set_tick_params(which='both', labelbottom=True)
    axs[1, 1].yaxis.set_tick_params(which='both', labelleft=True)
    axs[1, 1].legend()
    axs[0, 0].set(yticks=range(8), ylim=(0, 7), ylabel='layer index [-]')
    axs[1, 0].set(ylabel='layer index [-]')
    axs[0, 0].set_xlabel(r'$\mathregular{I_{abs,\/direct}}$' + '\n' + r'$\mathregular{[W \cdot m^{-2}]}$')
    axs[1, 1].set(xlabel=r'$\mathregular{I_{abs,\/sky-diffused}}$' + '\n' + r'$\mathregular{[W \cdot m^{-2}]}$',
                  ylabel='layer index [-]')
    axs[1, 2].set_xlabel(r'$\mathregular{I_{abs,\/leaf-scattered}}$' + '\n' + r'$\mathregular{[W \cdot m^{-2}]}$')

    fig2.tight_layout()
    fig2.subplots_adjust(wspace=0.1, hspace=0.2)
    fig2.savefig('absorbed_irradiance_components.png')
    plt.close('all')


if __name__ == '__main__':
    plot_results(set_shoot())
