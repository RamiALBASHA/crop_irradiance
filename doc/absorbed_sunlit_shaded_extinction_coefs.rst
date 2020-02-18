Extinction coefficients of irradiance components
================================================

Solar irradiance inside a crop canopy may be discretized into three distinct components: the **direct** (beam)
irradiance, the **diffuse** irradiance (solar irradiance diffused by the sky) and the **scattered** irradiance
(“second-hand” direct irradiance that has been dispatched by canopy elements).
Canopy leaf areas that are entirely exposed to the sun (sunlit) receive irradiance from all of direct, diffuse and
scattered components while shaded leaves receive only the diffuse and scattered components.
The extinction of each of the aforementioned irradiance components inside the canopy is estimated using Beer-Lambert’s
law, using extinction coefficients that are specific to each irradiance type.

One may say that the higher the sun in the sky is, the deeper sunflecks go through the canopy. It follows that the
extinction coefficient of direct irradiance inside the canopy depends on the inclination angle of the sun
:math:`\beta \ [-]`). In addition, the absorption of direct light by a sunlit surface depends on the angle
between the normal the surface and that of the solar beam, in a way that absorption is maxim when this angle is
0:math:`^\circ` (leaf surface is perpendicular to the solar beam), while it vanishes as it the angle approaches
90:math:`^\circ` (leaf surface is parallel to solar beam).
Considering that :math:`O_{av} \ [-]` is the average projection of canopy leaves in the direction of the solar beam,
and assuming leaves to act as perfect black surfaces (they absorb all the intercepted irradiance), the extinction
coefficient of direct irradiance :math:`k^{'}_{dir} \ [m^2_{ground} \cdot m^{-2}_{leaf}]` writes:

.. math::
    k^{'}_{dir} = \frac{O_{av}}{\sin{\beta}}

with :math:`O_{av}` given as:

.. math::
    :label: oav
    :flalign:

    O_{av} =&   \left \{
                    \begin{array}{11}
                        \sin \beta \cdot \cos \beta
                            & ; \ \beta \geq \alpha \\
                        \frac{2}{\pi} \cdot
                            \left(
                                {\sin \beta \cdot \cos \beta \cdot \arcsin \frac{\tan \beta}{\tan \alpha}
                                + \sqrt{\sin^2 \alpha + \sin^2 \beta}}
                            \right)
                                & ; \ \beta < \alpha \\
                    \end{array}
                \right.


where :math:`\alpha \ [-]` is leaf inclination angle in radians.

Assuming that canopy leaves are distributed in a manner that their surface perpendicular to the solar beam is constant
regardless of the solar inclination, i.e., their distribution of inclination is the same as that of surface elements
of the sphere **(de Wit, 1965)**, then the value of :math:`O_{av}` equals 0.5 **(Goudriaan, 1977)** and therefore:

.. math::
    k^{'}_{dir} = \frac{0.5}{\sin{\beta}}

The extinction coefficient calculated by the last equation applies only to the case where all leaves were black
(i.e. irradiance is neither transmitted through the leaves nor reflected by their surface). Nonetheless, for leaves
that have reflectance (:math:`\rho \[-]`) and transmittance (:math:`\tau \[-]`) ratios that are not null, a part or
direct irradiance is "scattered" by reflection and transmission by and through leaves, respectively.
As a result, the extinction of combined beam and scattered irradiance inside the canopy is less steeper than the "pure"
direct irradiance implying that the extinction coefficient (:math:`k_{dir} \ [m^2_{ground} \cdot m^{-2}_{leaf}]`) of
combined direct and scattered irradiance is smaller than that of the pure direct irradiance. **Cowan (1968)** defined
:math:`k_{dir}` as:

.. math::
    k_{dir} = k^{'}_{dir} \cdot \sqrt{1 - \sigma}

where
:math:`\sigma \ [-]` is leaf scattering coefficient, equal to the sum of leaf reflectance and transmittance, all in the
given irradiance band:

.. math::
    \sigma = \rho + \tau


The extinction coefficient of diffuse irradiance that comes from the sky
(:math:`k^{'}_{dif} \ [m^2_{ground} \cdot m^{-2}_{leaf}]`), is derived using the same procedure as for scattered
irradiance, but by considering the sky as an ensemble of finite sectors that send, each, diffuse irradiance as if it
were a beam irradiance. These sectors may be represented by rings. The extinction coefficient of diffuse irradiance
that is sent by each ring (:math:`k{'}_{dif, \ i}`) is calculated using **Eq. 4** by replacing the solar declination
:math:`\beta` by that of the sky ring (:math:`\beta_{sky, \ i \ [-]}`):

.. math::
    k^{'}_{dif, \ i} = \frac{O_{av}}{\sin{\beta_{sky, \ i}}}


Analogously to beam irradiance, as leaves may not be treated as purely black, the diffuse irradiance extinction
coefficient for none-black leaves (:math:`k_{dif} \ [m^2_{ground} \cdot m^{-2}_{leaf}]`) is smaller than that of black
ones. :math:`k_{dif}` is deduced from aggregating the diffuse profiles inside the canopy originating from all sky
rings :math:`n`:

.. math::
    k_{dif} = - \frac{1}{L_t} \cdot \ln
                \left(
                    \Sigma_i^n {c_i \cdot e^\left( {-k{'}_{dif, \ i} \sqrt{1 - \sigma}} \cdot L_t \right)}
                \right)

where
:math:`L_t \ [m^2_{leaf} \ m^{-2}_{ground}]` is the canopy total leaf area index and
:math:`c_i \ [-]` is a weighing factor accounting for the relative surface area of each sky ring.

**Goudriaan (1988)** showed that :math:`k_{dif}` is adequately estimated if the number of sky rings is greater or equal
to 3. Thus for 3 rings spanning respectively over angular sectors 0-30, 30-60 and 60-90:math:`^\circ`, **Eq. 10**
becomes:

.. math::
    k_{dif} = - \frac{1}{L_t} \cdot \ln
                \left(
                    0.178 \cdot e^ {-k{'}_{dif, \ 15} \sqrt{1 - \sigma} \cdot L_t}
                    + 0.514 \cdot e^ {-k{'}_{dif, \ 45} \sqrt{1 - \sigma} \cdot L_t}
                    + 0.308 \cdot e^ {-k{'}_{dif, \ 75} \sqrt{1 - \sigma} \cdot L_t}
                \right)

where
:math:`k^{'}_{dif, \ 15}`, :math:`k^{'}_{dif, \ 30}` and :math:`k^{'}_{dif, \ 45}` are values of :math:`k^{'}_{dif}`
for the central declination of each of the three ring sectors (i.e., 15, 45, 75:math:`^\circ`) and the coefficients
0.178, 0.514 and 0.308 are calculated for a standard sky over cast (SOC) assuming a ration 3:1 between zenith and
minimum horizontal sky illuminance.
