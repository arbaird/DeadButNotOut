from content.list_weapons import *

Pikeman={'Name':'Pikeman',
             'GroundMovement':4,
             'Flying':0,
             'TileNo':72,
             'Hitpoints':16,
             'Weapons':[Pike],
             'UnitFlags':0
             }

Citizen={'Name':'Citizen',
             'GroundMovement':4,
             'Flying':0,
             'TileNo':74,
             'Hitpoints':8,
             'Weapons':[Rake],
             'UnitFlags':0
             }

Beggar={'Name':'Beggar',
             'GroundMovement':4,
             'Flying':0,
             'TileNo':77,
             'Hitpoints':5,
             'Weapons':[Staff],
             'UnitFlags':0
             }

Warrior={'Name':'Warrior',
             'GroundMovement':4,
             'Flying':0,
             'TileNo':69,
             'Hitpoints':30,
             'Weapons':[FastBlow,Longsword],
             'UnitFlags':U_SLASH_RESISTANCE^U_BLUGDE_RESISTANCE
             }

Commander={'Name':'Commander',
             'GroundMovement':4,
             'Flying':0,
             'TileNo':63,
             'Hitpoints':30,
             'Weapons':[FastBlow,Longsword],
             'UnitFlags':U_SLASH_RESISTANCE
             }

Soldier={'Name':'Soldier',
             'GroundMovement':4,
             'Flying':0,
             'TileNo':85,
             'Hitpoints':18,
             'Weapons':[Longsword,Shortbow],
             'UnitFlags':U_MINOR_SLASH_RESISTANCE^U_MINOR_BLUGDE_RESISTANCE
             }

CentaurArcher={'Name':'Centaur Archer',
             'GroundMovement':6,
             'Flying':0,
             'TileNo':232,
             'Hitpoints':20,
             'Weapons':[Longbow],
             'UnitFlags':U_MINOR_BLUGDE_RESISTANCE
             }

CentaurWarrior={'Name':'Centaur Warrior',
             'GroundMovement':6,
             'Flying':0,
             'TileNo':233,
             'Hitpoints':57,
             'Weapons':[FastBlow,FastBlow,HeavyBlow],
             'UnitFlags':U_BLUGDE_RESISTANCE
             }

Angel={'Name':'Angel',
             'GroundMovement':6,
             'Flying':1,
             'TileNo':95,
             'Hitpoints':100,
             'Weapons':[AngelicSword,HolyRevenge],
             'UnitFlags':U_SLASH_RESISTANCE^U_BLUGDE_RESISTANCE^U_PIERCE_RESISTANCE
             }

WhiteMage={'Name':'White Mage',
             'GroundMovement':4,
             'Flying':0,
             'TileNo':70,
             'Hitpoints':15,
             'Weapons':[Healing],
             'UnitFlags':0
            }

