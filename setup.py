
from setuptools import setup, find_packages
from vaskitsa import __version__

setup(
    name='vaskitsa',
    keywords='python module maintenance',
    description='Initialize and maintain python modules',
    author='Ilkka Tuohela',
    author_email='hile@iki.fi',
    url='https://git.tuohela.net/code/vaskitsa',
    version=__version__,
    license='PSF',
    python_requires='>3.8.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'vaskitsa=vaskitsa.bin.main:main',
        ],
    },
    include_package_data=True,
    install_requires=(
        'inflection==0.5.1',
        'jinja2==3.0.2',
        'packaging==21.3',
        'requests==2.26.0',
        'pathlib-tree==1.1.0',
    ),
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Python Software Foundation License',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 3',
        'Topic :: System',
        'Topic :: System :: Systems Administration',
    ],
)
