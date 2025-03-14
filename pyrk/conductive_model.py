from pyrk.utilities.ur import units
from pyrk.materials.material import Material


class ConductiveModel(object):
    """
    This class defines models for conductive heat transfer coefficient: k
    """

    def __init__(self,
                 k0=0 * units.watt / units.meter / units.kelvin,
                 mat=Material(),
                 thickness=None,
                 area=None,
                 length=None,
                 inner_radius=None,
                 outer_radius=None,
                 model="constant"):
        """
        Initializes the ConductiveModel object.

        :param k0: thermal conductivity when using constant model
        :type k0: double with units of W/(m*K)
        :param mat: material of the component
        :type mat: Material object
        :param thickness: thickness of the conductive layer
        :type thickness: double with units of meters
        :param area: heat transfer surface area
        :type area: double with units of m^2
        :param length: length of the component (for cylindrical or rod geometries)
        :type length: double with units of meters
        :param inner_radius: inner radius (for cylindrical/spherical geometries)
        :type inner_radius: double with units of meters
        :param outer_radius: outer radius (for cylindrical/spherical geometries)
        :type outer_radius: double with units of meters
        :param model: The keyword for a model type, implemented types are
        'constant', 'plate', 'cylinder', and 'sphere'
        :type model: string
        """
        self.k0 = k0
        self.mat = mat
        self.thickness = thickness
        self.area = area
        self.length = length
        self.inner_radius = inner_radius
        self.outer_radius = outer_radius

        # Dictionary of implemented model types
        self.implemented = {
            'constant': self.constant,
            'plate': self.plate_conduction,
            'cylinder': self.cylindrical_conduction,
            'sphere': self.spherical_conduction
        }

        if model in self.implemented.keys():
            self.model = model
        else:
            self.model = NotImplemented
            msg = "Conductive heat transfer model type "
            msg += model
            msg += " is not an implemented conductive model. Options are: "
            for m in self.implemented.keys():
                msg += m + " "
            raise ValueError(msg)

    def conductance(self, temp=300 * units.kelvin):
        """
        Returns the thermal conductance based on the selected model
        and the component temperature.

        Conductance = (k*A)/L for simple geometries, with units of W/K

        :param temp: Temperature at which to evaluate material properties
        :type temp: float with units of kelvin
        """
        # Get the thermal conductivity at this temperature (if temperature-dependent)
        k = self.get_conductivity(temp)
        
        # Use the implemented model to calculate conductance
        return self.implemented[self.model](k)

    def get_conductivity(self, temp):
        """
        Returns the thermal conductivity at a given temperature.
        Uses either the constant k0 or the material's temperature-dependent k.

        :param temp: Temperature at which to evaluate conductivity
        :type temp: float with units of kelvin
        """
        if self.model == 'constant':
            return self.k0
        else:
            # Use the material's conductivity, which may be temperature-dependent
            return self.mat.k(temp)

    def constant(self, k):
        """
        Returns a constant thermal conductance
        
        :param k: Thermal conductivity
        :type k: float with units of W/(m*K)
        """
        return self.k0 * self.area / self.thickness

    def plate_conduction(self, k):
        """
        Calculates thermal conductance for a flat plate/wall geometry
        
        For flat geometries: Conductance = k*A/L
        
        :param k: Thermal conductivity
        :type k: float with units of W/(m*K)
        """
        if None in (self.area, self.thickness):
            raise ValueError("Area and thickness must be specified for plate conduction")
        
        return k * self.area / self.thickness

    def cylindrical_conduction(self, k):
        """
        Calculates thermal conductance for a cylindrical geometry (pipe/rod)
        
        For cylindrical geometries: Conductance = 2π*k*L/ln(r_o/r_i)
        
        :param k: Thermal conductivity
        :type k: float with units of W/(m*K)
        """
        if None in (self.length, self.inner_radius, self.outer_radius):
            raise ValueError("Length, inner_radius, and outer_radius must be specified for cylindrical conduction")
            
        import numpy as np
        return 2 * np.pi * k * self.length / np.log(self.outer_radius / self.inner_radius)

    def spherical_conduction(self, k):
        """
        Calculates thermal conductance for a spherical geometry
        
        For spherical geometries: Conductance = 4π*k*r_i*r_o/(r_o-r_i)
        
        :param k: Thermal conductivity
        :type k: float with units of W/(m*K)
        """
        if None in (self.inner_radius, self.outer_radius):
            raise ValueError("Inner_radius and outer_radius must be specified for spherical conduction")
            
        import numpy as np
        return 4 * np.pi * k * self.inner_radius * self.outer_radius / (self.outer_radius - self.inner_radius)

    def heat_flux(self, temp_hot, temp_cold):
        """
        Calculates the heat flux (W/m²) between two surfaces
        
        q" = k * (T_hot - T_cold) / thickness
        
        :param temp_hot: Temperature of the hot surface
        :type temp_hot: float with units of kelvin
        :param temp_cold: Temperature of the cold surface
        :type temp_cold: float with units of kelvin
        """
        k = self.get_conductivity((temp_hot + temp_cold) / 2)  # Evaluate k at average temperature
        
        if self.model == 'plate':
            return k * (temp_hot - temp_cold) / self.thickness
        else:
            # For non-plate geometries, use conductance and area
            conductance = self.conductance((temp_hot + temp_cold) / 2)
            if self.area is not None:
                return conductance * (temp_hot - temp_cold) / self.area
            else:
                raise ValueError("Area must be specified to calculate heat flux")
                
    def heat_rate(self, temp_hot, temp_cold):
        """
        Calculates the heat transfer rate (W) between two surfaces
        
        q = conductance * (T_hot - T_cold)
        
        :param temp_hot: Temperature of the hot surface
        :type temp_hot: float with units of kelvin
        :param temp_cold: Temperature of the cold surface
        :type temp_cold: float with units of kelvin
        """
        conductance = self.conductance((temp_hot + temp_cold) / 2)  # Evaluate at average temperature
        return conductance * (temp_hot - temp_cold)