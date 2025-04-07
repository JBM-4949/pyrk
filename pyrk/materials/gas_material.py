from pyrk.materials.material import Material
from pyrk.utilities.ur import units
from pyrk.density_model import DensityModel
from pyrk.inp import validation


class GasMaterial(Material):
    ''' subclass of material for gas'''

    def __init__(self,
                 name=None,
                 k=0 * units.watt / units.meter / units.kelvin,
                 cp=0 * units.joule / units.kg / units.kelvin,
                 dm=DensityModel(),
                 mu=0 * units.pascal * units.seconds):
#                 gamma=1.66,
#                 molar_mass=0 * units.kg / units.mol):
        """Initalizes a material

        :param name: The name of the component (i.e., "helium" or "nitrogen")
        :type name: str.
        :param k: The thermal conductivity of the component
        :type k: float, pint.unit.Quantity :math:'watt/meter/K'
        :param cp: specific heat capacity, :math:`c_p`, in :math:`J/kg-K`
        :type cp: float, pint.unit.Quantity :math:`J/kg-K`
        :param dm: The density model of the gas
        :type dm: DensityModel object
        :param mu: dynamic viscosity, :math:`mu`, in :math:`Pa.s`
        :type mu: float, pint.unit.Quantity :math:`Pa.s`
        :param gamma: heat capacity ratio (cp/cv)
        :type gamma: float
        :param molar_mass: molecular weight of the gas
        :type molar_mass: float, pint.unit.Quantity :math:`kg/mol`
        """
        Material.__init__(self, name, k, cp, dm)
        self.mu = mu.to('pascal*seconds')
#        self.gamma = gamma
#        self.molar_mass = molar_mass.to('kg/mol')
        validation.validate_ge("mu", mu, 0 * units.pascal * units.seconds)
#        validation.validate_gt("gamma", gamma, 1.0)
#        validation.validate_gt("molar_mass", molar_mass, 0 * units.kg / units.mol)
