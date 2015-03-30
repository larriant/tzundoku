import os, sys

PROHECT_DIR = '/www/staging.julyandavey.com/index.py'

activate_this = os.path.join(PROJECT_DIR, 'bin', 'activate_this.py')
execfile(activate_this, dict(__file__=activate_this))
sys.path.append(PROJECT_DIR)

from index.py import app as application


