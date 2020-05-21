from setuptools import setup, find_packages

setup(
    name='Demonstrator',
    version='0.1.5',
    packages=find_packages(),
    url='',
    license='MIT',
    author='Daniel, Ben, Victor, Sohrab, Ruben, Jean-Paul',
    author_email='',
    package_data={'': ['*.txt', '*.PNG']},
    include_package_data=True,
    description='',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: MIT License",
        "Operating System :: Raspberry Pi",

    ],
    install_requires=[
        'matplotlib',
        'numpy',
        'paho-mqtt',
        'pvlib',
        'pandas',
        'requests',
        'plotly',
        'dash',
    ],
    # install_requires=['peppercorn'] #what is needed minimally to run this
)
