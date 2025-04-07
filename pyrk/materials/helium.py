from pyrk.utilities.ur import units
from pyrk.density_model import DensityModel
from pyrk.materials.liquid_material import LiquidMaterial
#from pyrk.materials.gas_material import GasMaterial

class Helium(LiquidMaterial):
    """This class represents FLiBe. It inherits from the material
    class and possesses attributes intrinsic to flibe.

    Reference:
    Williams, D. F., Toth, D. M. and Clarno, K. T. Assessment of Candidate
    Molten Salt Coolants for the Advanced High-Temperature Reactor (AHTR).s.l.
    Oakridge National Laboratory Technical Report, March 2006. ORNL/TM-2006/12.
    Sohal MS, Ebner MA, Sabharwall P, Shape P (INL).
    Engineering Database of Liquid Salt Thermophysical and Thermochemical
    Properties. INL/EXT-10 18297. March 2010.
    Allen, T. Molten Salt Database,
    http://allen.neep.wisc.edu/shell/index.php/salts,
    Nuclear Engineering and Engineering Physics Department,
    University of Wisconsin. 2010
    P. Bardet et al. Dynamics of liquid-protected fusion chambers.
    Fusion science and technology, vol 47, 2005.
    """

    def __init__(self, name="helium"):
        """Initalizes a material

        :param name: The name of the component (i.e., "fuel" or "cool")
        :type name: str.
        """
        LiquidMaterial.__init__(self,
                                name=name,
                                k=self.thermal_conductivity(),
                                cp=self.specific_heat_capacity(),
                                dm=self.density())

    def thermal_conductivity(self):
        """FLiBe thermal conductivity in [W/m-K]
        TODO:k= 0.7662+0.0005T (T in celsius)
        """
        #
        return 1.0 * units.watt / (units.meter * units.kelvin)

    def specific_heat_capacity(self):
        """Specific heat capacity of flibe [J/kg/K]
        """
        #htr
        return 5.1932 * units.joule / (units.kg * units.kelvin)

    def density(self):
        """
        # HTRPM
        
        Helium density as a funciton of T. [kg/m^3]
        17.8 + -0.0356x + 3.12E-05x^2 + -1.01E-08x^3

        """
        return DensityModel(a=17.8 * units.kg / (units.meter**3),
                            b=-0.0356 * units.kg /
                            (units.meter**3) / units.kelvin,
#                            c=0.0000312 * units.kg /
#                            (units.meter**3) / units.kelvin,
#                            d=-0.0000000101 * units.kg /
#                            (units.meter**3) / units.kelvin,
                            model="linear")
