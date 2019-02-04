# Test of Absolute Imports
# Doc tree:
"""
|---primary level
    |--- __init__.py
    |--- primarylevel.py
    |
    |--- secondarylevel
    |   |--- __init__.py
    |   |--- secondarylevel.py
    |
    |--- tertiarylevel
    |   |--- __init__.py
    |   |--- tertiarylevel.py
    |
    |--- fourthlevel
        |--- __init__.py
        |--- fourthlevel.py
        |--- relativetry.py
    
"""

from secondarylevel import secondarylevel
import tertiarylevel.tertiarylevel

print("Primary level")

secondarylevel.dothis()
tertiarylevel.tertiarylevel.dothis()

# Test of Dynamic Imports

_temp = __import__('fourthlevel.fourthlevel',globals(),locals(),['dothis'],0)
doit = _temp.dothis
doit()

    # OR

_temp = __import__('fourthlevel',globals(),locals(),['fourthlevel'],0)
doit = _temp.fourthlevel
doit.dothis()

    # OR dynamically setting import

tgtfile = 'fourthlevel'
_temp = __import__('fourthlevel',globals(),locals(),[tgtfile],0)
doit = _temp.fourthlevel
doit.dothis()

# Test of Relative Imports