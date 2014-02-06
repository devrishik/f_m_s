from fabric.api import local, env, settings, cd, run, sudo, get

env.project_name = 'fixme' # use parent folder name?

env.db_user = 'singh'
env.db_password = 'password'
env.db_host = 'localhost'
env.db_name = env.project_name

# Default to dev/local
env.user = 'ubuntu'
# env.hosts = ['dev.fixme.ophio.co.in']
# env.deploy_branch = 'dev'
env.django_settings = 'fixme.settings.dev'

env.use_ssh_config = True
env.requirements_file = 'requirements/dev.txt'


# ==========================================================================
#  Environment
# ==========================================================================

# def production():
#     env.hosts = ['fixmeapp.com']
#     env.django_settings = 'fixme.settings.production'
#     env.requirements_file = 'requirements/production.txt'
#     env.deploy_branch = 'master'


# ==========================================================================
#  TASKS
# ==========================================================================
def setup(db=True):
    '''Use this to setup the project for the first time after cloning the project.'''
    local('virtualenv venv')
    install_requirements()
    if(db):
        create_db()
    manage('syncdb')
    manage('migrate')

def install_requirements():
    local('source venv/bin/activate && pip install -r requirements/local.txt')

def serve():
    manage('runserver')


def shell():
    '''Start a django shell using shell_plus from django_extensions'''
    manage('shell_plus')


def new_migration(app='core'):
    manage('schemamigration core --auto')
    manage('migrate core')

def create_db():
    with settings(warn_only=True):
        local("mysql -uroot -p -e \"CREATE DATABASE %(db_name)s\" -h %(db_host)s" % env)
        local("mysql -uroot -p -e \"CREATE USER '%(db_user)s'@'%(db_host)s' identified by '%(db_password)s'\"" % env)
        local("mysql -uroot -p -e \"GRANT ALL on %(db_name)s.* to '%(db_user)s'@'%(db_host)s'\"" % env)

def manage(cmd):
    local('source venv/bin/activate && python {project_name}/manage.py {cmd}'.format(
            project_name=env.project_name,
            cmd=cmd
        ))

def server_restart():
    sudo("service apache2 restart")


def get_db_dump():
    run('mysqldump --compatible=postgresql --default-character-set=utf8 -h fueled.cnf7uruewtae.us-east-1.rds.amazonaws.com -u fixme_dev -ppassword fixme_dev > /tmp/sql.dump')
    get('/tmp/sql.dump')


# def deploy():
#     '''
#     Deploy the code on server, default to development server.
#     '''
#     test()
#     local('git push')
#     with cd('/opt/webapps/fixme/'):
#         run('git reset --hard')
#         run('git checkout %(deploy_branch)s' % env)
#         run('git fetch')
#         run('git rebase origin/%(deploy_branch)s' % env)
#         sudo('pip install -r %(requirements_file)s' % env)
#         run("python %(project_name)s/manage.py migrate --settings='%(django_settings)s'" % env)
#         run("python %(project_name)s/manage.py collectstatic --noinput --settings='%(django_settings)s'" % env)
#         sudo("service apache2 restart")

def test():
    manage('test --settings=%(project_name)s.settings.test' % env)
