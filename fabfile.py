from __future__ import with_statement
from fabric.api import local, run, cd, env


env.user = "bayo"
env.password = "pass.p455"
env.hosts = ["bayo.webfactional.com"]


def push():
    local("python manage.py test")
    local("git add -p && git commit")
    local("git push")


def deploy():
    local("git push")
    remote_dir = '/home/bayo/webapps/roundtable/yarep/'
    with cd(remote_dir):
        run("git pull -u")
        run("python2.7 manage.py syncdb --migrate")
        run("python2.7 manage.py collectstatic --noinput")
        run("../apache2/bin/restart")
