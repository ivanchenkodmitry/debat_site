#!/usr/bin/env python
import sys, os

from os.path import abspath, dirname, join


_PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, "/home/nskrypnik/pinax/Pinax-0.7.3-bundle/pinax-env/lib/python2.6/site-packages/pinax/apps")
sys.path.insert(0, "/home/nskrypnik/pinax/Pinax-0.7.3-bundle/pinax-env/lib/python2.6/site-packages/pinax/projects/social_project/apps")
sys.path.insert(0, "/home/nskrypnik/pinax/Pinax-0.7.3-bundle/pinax-env/lib/python2.6/site-packages/pinax")
sys.path.insert(0, "/home/nskrypnik/pinax/Pinax-0.7.3-bundle/pinax-env/lib/python2.6/site-packages/")
sys.path.insert(0, _PROJECT_DIR + "/apps")
sys.path.insert(0, _PROJECT_DIR)
sys.path.insert(0, os.path.dirname(_PROJECT_DIR))


try:
    import pinax
except ImportError:
    sys.stderr.write("Error: Can't import Pinax. Make sure you are in a virtual environment that has Pinax installed or create one with pinax-boot.py.\n")
    sys.exit(1)

from django.conf import settings
from django.core.management import setup_environ, execute_from_command_line

try:
    import settings as settings_mod # Assumed to be in the same directory.
except ImportError:
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
    sys.exit(1)

# setup the environment before we start accessing things in the settings.
setup_environ(settings_mod)

sys.path.insert(0, join(settings.PINAX_ROOT, "apps"))
sys.path.insert(0, join(settings.PROJECT_ROOT, "apps"))

if __name__ == "__main__":
    execute_from_command_line()
