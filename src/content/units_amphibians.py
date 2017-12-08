from content.list_weapons import *

SpectralToad={'Name':'Spectral Toad',
          'GroundMovement':5,
          'Flying':0,
          'TileNo':129,
          'Hitpoints':20,
          'Weapons':[ToadTongue,ToadSacrifice],
          'UnitFlags':U_POISON_RESISTANCE^U_BLUGDE_RESISTANCE^U_SPECTRAL
          }


WarToad={'Name':'War Toad',
          'GroundMovement':3,
          'Flying':0,
          'TileNo':130,
          'Hitpoints':22,
          'Weapons':[ToadTongue],
          'UnitFlags':U_POISON_RESISTANCE^U_MINOR_BLUGDE_RESISTANCE
          }

GiantToad={'Name':'Giant Toad',
          'GroundMovement':4,
          'Flying':0,
          'TileNo':131,
          'Hitpoints':20,
          'Weapons':[ToadSpit],
          'UnitFlags':U_POISON_RESISTANCE
          }

HeavyWarToad={'Name':'Heavy Wartoad',
             'GroundMovement':4,
             'Flying':0,
             'TileNo':132,
             'Hitpoints':62,
             'Weapons':[ToadStinger,ToadSacrifice],
             'UnitFlags':U_POISON_RESISTANCE^U_BLUGDE_RESISTANCE
             }

BloatedFloater={'Name':'Bloated Floater',
             'GroundMovement':4,
             'Flying':1,
             'TileNo':59,
             'Hitpoints':100,
             'Weapons':[FloaterTouch,FloaterExplosion],
             'UnitFlags':U_POISON_RESISTANCE
             }
