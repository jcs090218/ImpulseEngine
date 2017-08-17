import os
import sys

# get current file path
current_file_path=os.path.dirname(os.path.realpath(__file__))

# replace '\' to '/'
current_file_path = current_file_path.replace('\\', '/')

# find the '.egg' using relative path.
jcspygm_egg_path=current_file_path + "/../lib/jcspygm-1.0.2-py2.7.egg"

# add it to 'PYTHON_PATH'
sys.path.append(jcspygm_egg_path)


# -------------------------
# Absolute Path

# If you want export to executable need to use absolute path.
jcspygm_egg_abs_path = "C:/DataBase_Enterprise/Asia/ALDES/ALDES_Entertainment/BaseEngine/Eclipse_Neon/JCSPyGm_Physics/lib/jcspygm-1.0.2-py2.7.egg"

sys.path.append(jcspygm_egg_abs_path)
