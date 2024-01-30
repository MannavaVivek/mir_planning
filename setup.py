import os
from glob import glob
from setuptools import setup

package_name = 'mir_planning'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'config'), 
         glob(os.path.join('config', '*'))),
        (os.path.join('lib', package_name, 'actions'), 
         glob(os.path.join('mir_planning/actions', '*'))),
        (os.path.join('share', package_name, 'launch'), 
         glob(os.path.join('launch', '*launch.[pxy][yma]*')))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='vivek',
    maintainer_email='vivekmannava@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'mir_planner_executor = mir_planning.mir_planner_executor:main',
            'lc_planner_executor = mir_planning.mir_planner_executor_lifecycle:main'
        ],
    },
)
