from content.list_weapons import *

GrimSkeleton={'Name':'Grim Skeleton',
              'GroundMovement':5,
              'Flying':0,
              'TileNo':27,
              'Hitpoints':19,
              'Weapons':[UndeadScythe],
              'UnitFlags':U_PIERCE_RESISTANCE^U_SLASH_RESISTANCE^U_UNDEAD
              }
RedImp={'Name':'Fire Imp',
              'GroundMovement':5,
              'Flying':1,
              'TileNo':45,
              'Hitpoints':12,
              'Weapons':[DevilSpark,HeatTouch],
              'UnitFlags':0
              }

GreenImp={'Name':'Acid Imp',
              'GroundMovement':5,
              'Flying':1,
              'TileNo':48,
              'Hitpoints':12,
              'Weapons':[AcidTouch],
              'UnitFlags':0
              }

BlackImp={'Name':'Night Imp',
              'GroundMovement':5,
              'Flying':1,
              'TileNo':49,
              'Hitpoints':12,
              'Weapons':[DarknessTouch],
              'UnitFlags':0
              }
WhiteImp={'Name':'Ice Imp',
              'GroundMovement':5,
              'Flying':1,
              'TileNo':51,
              'Hitpoints':12,
              'Weapons':[IceTouch],
              'UnitFlags':0
              }

MinorDevil={'Name':'Minor Devil',
              'GroundMovement':5,
              'Flying':1,
              'TileNo':41,
              'Hitpoints':17,
              'Weapons':[DevilSpark,Fireball],
              'UnitFlags':0
              }

Abomination={'Name':'Abomination',
             'GroundMovement':4,
             'Flying':0,
             'TileNo':208,
             'Hitpoints':62,
             'Weapons':[TentacularStroke,TentacularStroke,VampireBite],
             'UnitFlags':U_POISON_RESISTANCE^U_UNDEAD
             }

Lich={NAME:'Lich',
      GM:3,
      FLY:1,
      TILE:5,
      WEAPONS:[WrathTouch,WrathFlame],
      HP:30,
      NUNITFLAGS:U_UNDEAD}

Vampire={'Name':'Vampire',
             'GroundMovement':5,
             'Flying':1,
             'TileNo':197,
             'Hitpoints':30,
             'Weapons':[VampireBite],
             'UnitFlags':U_MINOR_BLUGDE_RESISTANCE^U_UNDEAD
             }
Horror={'Name':'Horror',
             'GroundMovement':6,
             'Flying':0,
             'TileNo':10,
             'Hitpoints':70,
             'Weapons':[UndeadStitch,UndeadStitch,VampireBite],
             'UnitFlags':U_UNDEAD^U_SPECTRAL^U_CRITIMMUN
             }
