# pinax.wsgi is configured to live in projects/testsite/deploy.

import os
import sys

# redirect sys.stdout to sys.stderr for bad libraries like geopy that uses
# print statements for optional import exceptions.
sys.stdout = sys.stderr

from os.path import abspath, dirname, join
from site import addsitedir

sys.path.insert(0, abspath(join(dirname(__file__), "../../")))

from django.conf import settings
#os.environ["DJANGO_SETTINGS_MODULE"] = "debat_site.settings"

#sys.path.insert(0, join(settings.PINAX_ROOT, "apps"))
#sys.path.insert(0, join(settings.PROJECT_ROOT, "apps"))

_PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(0, "/home/dmitry/pinax/Pinax-0.7.3-bundle/pinax-env/lib/python2.6/site-packages/pinax/projects/social_project/apps")
sys.path.insert(0, "/home/dmitry/pinax/Pinax-0.7.3-bundle/pinax-env/lib/python2.6/site-packages/pinax")
sys.path.insert(0, "/home/dmitry/pinax/Pinax-0.7.3-bundle/pinax-env/lib/python2.6/site-packages/")

sys.path.insert(0, '/home/dmitry/pinax/Pinax-0.7.3-bundle/pinax-env/lib/python2.6/lib-dynload')
sys.path.insert(0, '/home/dmitry/pinax/Pinax-0.7.3-bundle/pinax-env/lib/python2.6/lib-old')
sys.path.insert(0, '/home/dmitry/pinax/Pinax-0.7.3-bundle/pinax-env/lib/python2.6/lib-tk')
sys.path.insert(0, '/home/dmitry/pinax/Pinax-0.7.3-bundle/pinax-env/lib/python2.6/plat-linux2')
sys.path.insert(0, '/home/dmitry/pinax/Pinax-0.7.3-bundle/pinax-env/lib/python2.6')
sys.path.insert(0, '/home/dmitry/pinax/Pinax-0.7.3-bundle/pinax-env/lib/python2.6/site-packages/pip-0.6.1-py2.6.egg')
sys.path.insert(0, '/home/dmitry/pinax/Pinax-0.7.3-bundle/pinax-env/lib/python2.6/site-packages/setuptools-0.6c11-py2.6.egg')

sys.path.insert(0, _PROJECT_DIR)
sys.path.insert(0, "/home/dmitry/pinax/Pinax-0.7.3-bundle/pinax-env/lib/python2.6/site-packages/pinax/apps")
sys.path.insert(0, _PROJECT_DIR + "/apps")


_PROJECT_NAME = _PROJECT_DIR.split('/')[-1]
os.environ['DJANGO_SETTINGS_MODULE'] = "%s.settings" % _PROJECT_NAME

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()
