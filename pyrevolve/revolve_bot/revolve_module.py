"""
Class containing the body parts to compose a Robogen robot
"""

from collections import OrderedDict

class RevolveModule():
    """
    Base class allowing for constructing Robogen components in an overviewable manner
    """
    DEFAULT_COLOR = (0.5, 0.5, 0.5)
    TYPE = 'NONE'

    def __init__(self):
        self.id = None
        self.slot = None
        self.orientation = None
        self.rgb = None #RevolveModule.DEFAULT_COLOR
        self.substrate_coordinates = None
        self.children = [None, None, None, None]

    def color(self):
        return self.rgb if self.rgb is not None else self.DEFAULT_COLOR

    @staticmethod
    def FromYaml(yaml_object):
        mod_type = yaml_object['type']
        if mod_type == 'CoreComponent' or mod_type == 'Core':
            module = CoreModule()
        elif mod_type == 'ActiveHinge':
            module = ActiveHingeModule()
        elif mod_type == 'FixedBrick':
            module = BrickModule()
        elif mod_type == 'FixedBrickSensor':
            module = BrickSensorModule()
        else:
            raise NotImplementedError('"{} module not yet implemented'.format(mod_type))

        module.id = yaml_object['id']

        try:
            module.slot = yaml_object['slot']    
        except KeyError:
            module.slot = 0

        try:
            module.orientation = yaml_object['orientation']
        except KeyError:
            module.orientation = 0

        try:
            module.rgb = (
                yaml_object['params']['red'],
                yaml_object['params']['green'],
                yaml_object['params']['blue'],
            )
        except KeyError:
            pass

        if 'children' in yaml_object:
            for parent_slot in yaml_object['children']:
                module.children[parent_slot] = RevolveModule.FromYaml(
                    yaml_object=yaml_object['children'][parent_slot])

        return module

    def to_yaml(self):
        yaml_dict_object = OrderedDict()
        yaml_dict_object['id'] = self.id
        yaml_dict_object['type'] = self.TYPE
        yaml_dict_object['slot'] = self.slot
        yaml_dict_object['orientation'] = self.orientation

        if self.rgb is not None:
            yaml_dict_object['params'] = { 
                'red': self.rgb[0],
                'green': self.rgb[1],
                'blue': self.rgb[2],
            }

        children = self.generate_yaml_children()
        if children is not None:
            yaml_dict_object['children'] = children
        
        return yaml_dict_object

    def generate_yaml_children(self):
        has_children = False

        children = {}
        for i, child in enumerate(self.children):
            if child is not None:
                children[i] = child.to_yaml()
                has_children = True

        return children if has_children else None

    def validate(self):
        """
        Tests if the robot tree is valid (recursively)
        :return: True if the robot tree is valid
        """
        raise NotImplementedError("robot tree validation not yet implemented")

    def to_sdf(self):
        """

        :return:
        """

        return ''


class CoreModule(RevolveModule):
    """
    Inherits class RevolveModule. Creates Robogen core module
    """
    TYPE = "CoreComponent"

    def __init__(self):
        super().__init__()


class ActiveHingeModule(RevolveModule):
    """
    Inherits class RevolveModule. Creates Robogen joint module
    """
    TYPE = "ActiveHinge"

    def __init__(self):
        super().__init__()
        self.children = {1: None}

    def generate_yaml_children(self):
        child = self.children[1]
        if child is None:
            return None
        else:
            return {1: child.to_yaml()}


class BrickModule(RevolveModule):
    """
    Inherits class RevolveModule. Creates Robogen brick module
    """
    TYPE = "FixedBrick"

    def __init__(self):
        super().__init__()


class BrickSensorModule(RevolveModule):
    """
    Inherits class RevolveModule. Creates Robogen brick sensor module
    """
    TYPE = "FixedBrickSensor"

    def __init__(self):
        super().__init__()