from setuptools import setup, find_packages

setup(
    name='time_series_lib',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'scipy',
        'matplotlib',
        'seaborn',
        'statsmodels'
    ],
    description='Library for time series analysis',
    author='Pavel Malyshev',
    author_email='p.malyshev@razumai.pro',
    url='https://github.com/PavelMalyshev01/time_series_lib',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
