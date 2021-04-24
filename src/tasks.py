from invoke import task

@task
def clean(c, docs=False, bytecode=False, extra=''):
    patterns = ['build']
    if docs:
        patterns.append('docs/_build')
    if bytecode:
        patterns.append('**/*.pyc')
    if extra:
        patterns.append(extra)
    for pattern in patterns:
        c.run("rm -rf {}".format(pattern))

@task
def start(c, docs=False):
    # c.run("python manage.py runserver 0.0.0.0:8000")
    c.run("gunicorn main.wsgi --bind 0.0.0.0:8000")

    
@task
def install(c, docs=False):
    c.run("python manage.py makemigrations")
    c.run("python manage.py migrate")
    c.run("python manage.py initadmin")
    c.run("python manage.py collectstatic --no-input")
    
@task
def connect(c, docs=False):
    c.run("source ./wait-for-posgre.sh")