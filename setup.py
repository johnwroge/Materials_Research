from setuptools import setup, find_packages

setup(
    name="materials_aggregator",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pymatgen>=2022.0.0",
        "pandas>=1.3.0",
        "matplotlib>=3.4.0",
        "seaborn>=0.11.0",
        "tabulate>=0.8.9",
        "requests>=2.25.0",
        "numpy>=1.20.0",
        "scipy>=1.7.0",
        "plotly>=5.3.0",
    ],
    entry_points={
        'console_scripts': [
            'materials_aggregator=materials_aggregator.cli:main',
        ],
    },
    python_requires='>=3.7',
    author="John Wroge",
    author_email="wrogejohn@gmail.com",
    description="A tool for chemists to aggregate materials research information from the Materials Project",
    keywords="materials science, chemistry, materials project, data analysis",
    url="https://github.com/johnwroge/materials-research-aggregator",
)