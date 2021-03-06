from content.list_unit_config import *



Rake={'Name':'Rusty Rake',
              'Type':SLASHING,
              'Damage':3,
              'Flags':F_NONE,
              'Range':1}


UndeadStitch={'Name':'Stitch',
              'Type':PIERCING,
              'Damage':6,
              'Flags':F_FREEATTACK^F_LIVEDRAINING,
              'Range':1}

Staff={'Name':'Staff',
              'Type':BLUDGEONING,
              'Damage':2,
              'Flags':0,
              'Range':1}

Pike={'Name':'Pike',
              'Type':PIERCING,
              'Damage':7,
              'Flags':F_SUPERKRIT,
              'Range':2}

IllithidBite={'Name':'Illithid Bite',
              'Type':PIERCING,
              'Damage':5,
              'Flags':F_ENSLAVE,
              'Range':1}

IllithidTentacle={'Name':'Illithid Tentacle',
              'Type':BLUDGEONING,
              'Damage':5,
              'Flags':F_FREEATTACK,
              'Range':1}

HolyStrike={'Name':'Holy Strike',
              'Type':TOUCH,
              'Damage':8,
              'Flags':0,
              'Range':3}

Healing={'Name':'Cure wounds',
              'Type':TOUCH,
              'Damage':6,
              'Flags':F_HEAL,
              'Range':1}

AngelicSword={'Name':'Angelic Sword',
              'Type':SLASHING,
              'Damage':15,
              'Flags':F_FREEATTACK,
              'Range':1}

AngelicBlow={'Name':'Angelic Blow',
              'Type':SLASHING,
              'Damage':20,
              'Flags':F_SUPERKRIT,
              'Range':1}

HolyRevenge={'Name':'Holy Revenge',
              'Type':TOUCH,
              'Damage':25,
              'Flags':F_EXHAUSTING,
              'Range':3}

Longsword={'Name':'Longword',
              'Type':SLASHING,
              'Damage':7,
              'Flags':F_NONE,
              'Range':1}

FastBlow={'Name':'Fast Blow',
              'Type':SLASHING,
              'Damage':6,
              'Flags':F_FREEATTACK,
              'Range':1}

HeavyBlow={'Name':'Heavy Blow',
           'Type':SLASHING,
           'Damage':15,
           'Flags':F_SUPERKRIT,
           'Range':1}

Shortbow={'Name':'Shortbow',
              'Type':PIERCING,
              'Damage':5,
              'Flags':F_NONE,
              'Range':2}

Longbow={'Name':'Longbow',
         'Type':PIERCING,
         'Damage':9,
         'Flags':F_SUPERKRIT,
         'Range':2}

HeatTouch={'Name':'Touch of Heat',
         'Type':TOUCH,
         'Damage':3,
         'Flags':F_FIRE,
         'Range':1}

AcidTouch={'Name':'Touch of Acid',
         'Type':TOUCH,
         'Damage':3,
         'Flags':F_POISON,
         'Range':1}

DarknessTouch={'Name':'Touch of Darkness',
         'Type':TOUCH,
         'Damage':3,
         'Flags':F_ENSLAVE,
         'Range':1}

IceTouch={'Name':'Devils Spark',
         'Type':TOUCH,
         'Damage':4,
         'Flags':F_DEATHTOUCH,
         'Range':1}

DevilSpark={'Name':'Devils Spark',
         'Type':TOUCH,
         'Damage':2,
         'Flags':F_FREEATTACK^F_FIRE,
         'Range':1}

Fireball={'Name':'Fireball',
         'Type':TOUCH,
         'Damage':10,
         'Flags':F_FIRE,
         'Range':3}



UndeadScythe={'Name':'Undead Scythe',
              'Type':SLASHING,
              'Damage':6,
              'Flags':F_SUPERKRIT,
              'Range':1}

WrathTouch={'Name':'Wrath Touch',
            'Type':TOUCH,
            'Damage':15,
            'Flags':F_DEATHTOUCH,
            'Range':1}

WrathFlame={'Name':'Wrath Flame',
            'Type':TOUCH,
            'Damage':10,
            'Flags':F_DEATHTOUCH,
            'Range':2}

TentacularStroke={'Name':'Tentacular Stroke',
                  'Type':BLUDGEONING,
                  'Damage':5,
                  'Range':1,
                  'Flags':F_FREEATTACK^F_POISON}

ToadStinger={'Name':'Toad Stinger',
            'Type':PIERCING,
            'Damage':18,
            'Flags':F_POISON,
            'Range':1}

#adilen the toadgod

ToadSacrifice={'Name':'Sacrifice to Adilen',
            'Type':TOUCH,
            'Damage':20,
            'Flags':F_POISON^F_SACRIFICE,
            'Range':1}

ToadTongue={'Name':'Toad Tongue',
            'Type':BLUDGEONING,
            'Damage':8,
            'Flags':F_NONE,
            'Range':1}

ToadSpit={'Name':'Toad Spit',
            'Type':TOUCH,
            'Damage':5,
            'Flags':F_POISON,
            'Range':2}


HolyStrike={'Name':'Holy Strike',
              'Type':TOUCH,
              'Damage':8,
              'Flags':0,
              'Range':3}

Bite={'Name':'Bite',
      'Type':PIERCING,
      'Damage':10,
      'Range':1,
      'Flags':F_LIVEDRAINING}

VampireBite={'Name':'Vampirebite',
      'Type':PIERCING,
      'Damage':10,
      'Range':1,
      'Flags':F_LIVEDRAINING}

FloaterTouch={'Name':'Nasty Touch',
      'Type':TOUCH,
      'Damage':12,
      'Range':1,
      'Flags':F_POISON^F_LIVEDRAINING}

FloaterExplosion={'Name':'Sacrifice',
      'Type':TOUCH,
      'Damage':45,
      'Range':1,
      'Flags':F_SACRIFICE}