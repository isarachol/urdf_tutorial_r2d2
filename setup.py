import os
from glob import glob
from setuptools import setup
from setuptools import find_packages
from setuptools import find_packages, setup

package_name = 'urdf_tutorial_r2d2'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'),
            glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
  	    (os.path.join('share', package_name, 'urdf'), glob('urdf/*')),
  	    (os.path.join('share', package_name, 'description'), glob('description/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='tand',
    maintainer_email='tand.isara2001@gmail.com',
    description='Learning URDF, ros_launch, joint_state_publisher, robot_state_publisher, and rviz',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'state_publisher = urdf_tutorial_r2d2.state_publisher:main',
            'multi_state_publisher = urdf_tutorial_r2d2.multi_state_publisher:main'
        ],
    },
)
