from setuptools import setup

setup(
    name='quadtree',
    version='1.0',
    description='QuadTree library',
    author='Omar Aflak',
    author_email='aflakomar@gmail.com',
    packages=['quadtree'],
    install_requires=[
        'geometry @ git+https://github.com/omaraflak/geometry'
    ]
)
