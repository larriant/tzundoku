from fabric.api import env, run, cd

USERNAME = 'root'
SERVER = 'staging.julyandavey.com'
APP_NAME = 'tzundoku'
PROJECT_DIR = '/srv/staging.julyandavey.com/public/htdocs/tzundoku'
WSGI_SCRIPT = 'application.wsgi'

env.hosts = ["%s@%s" (USERNAME, SERVER)]

def deploy():
    with cd(PROJECT_DIR):
	run('git pull')
	run('bin source/activate')
	run('pip install -r requirements.txt')
	run('touch %s' % WSGI_SCRIPT)
