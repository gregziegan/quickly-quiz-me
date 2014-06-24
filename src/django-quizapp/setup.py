from setuptools import setup, find_packages

setup(
    name = "django-quizapp",
    version = "0.1",
    url = '',
    license = 'Private',
    description = "A multiplayer quiz application",
    author = 'Greg Ziegan',
    packages = ['quizapp', 'quizapp.management', 'quizapp.management.commands'],
    package_dir = {'django-quizapp': 'quizapp'},
    install_requires = ['setuptools'],
)
