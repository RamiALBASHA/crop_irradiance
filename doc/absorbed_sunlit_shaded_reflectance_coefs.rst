Reflectance coefficients of irradiance components
=================================================
Canopy reflectance to direct irradiance :math:`\rho_{dir} \ [-]` depends on leaf angles distribution and the declination of
the solar beam. :math:`\rho_{dir}` is lowest when the sun is closest the zenith and highest as solar inclination
approaches 0 :math:`^\circ` (sun is grazing over horizontal leaves). :math:`\rho_{dir}` is given by **Goudriaan (1977)**
as:

.. math::
    :label: direct_canopy_reflectance
    \rho_{dir} = 1 - \exp{
        \left(
            - \frac{2 \cdot \rho_h \cdot k^{'}_{dir}}{1 + k^{'}_{dir}}
        \right)
    }

where :math:`\rho_h \ [-]` is the reflection coefficient of a canopy having horizontal leaves, defined as:

.. math::
    :label: horizontal_reflectance

    \rho_h = \frac{1 - \sqrt{1 - \sigma}}{1 + \sqrt{1 - \sigma}}


Canopy reflectance coefficient to diffuse irradiance (:math:`\rho_{dif}`) may be deduced using
:eq:`direct_canopy_reflectance` by aggregating reflectance coefficients relative to all sky rings (analogously to the
method of deducing :math:`k_{dif}` from :math:`k^{'}_{dir}`):

.. math::
    :label: diffuse_canopy_reflectance

    \rho_{dif} = \frac{1}{I_{dif}} \int_0^{\pi/2} {I_{dif} \cdot c_{\beta_{sky}} \cdot \rho_{dir, \ \beta_{sky}} \ d\beta_{sky}}

where
:math:`I_{inc, \ dif} \ [W \cdot m^{-2}_{ground}]` is the incident diffuse irradiance,
:math:`c_{\beta_{sky}} \ [-}` is a weighing factor accounting for the relative surface area of each sky elevation, and
:math:`\beta_{sky} \ [-]` is the elevation angle of a sky ring of a finite height.

For a spherical leaf inclination distribution and under a sky overcast, **Goudriaan and van Laar (1994)** found that
the value of :math:`\rho_{dif}` equals 0.057 within the photosynthetically active radiation (PAR) band and 0.389 for
the near infrared (NIR) band. These values are set as constants for :math:`\rho_{dif}` and the equation
:eq:`diffuse_canopy_reflectance` is not used.