import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__))+"\\..\\..\\..\\Maxime\\Trames_Piseo\\")
from CEtuve import Etuve
try:
    client = Etuve("0.0.0.0",0)
    print("a")
except:
    print("b")
