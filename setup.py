import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="crop_irradiance",
    version="0.0.1",
    author="Rami ALBASHA",
    author_email="rami albacha at yahoo dot com",
    description="a library for simulating irradiance absorption by crops canopies",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RamiALBASHA/crop_irradiance",
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: CeCILL-C Free Software License Agreement (CECILL-C)",
        "Operating System :: OS Independent",
    ],
    install_requires=[
    ],
    tests_require=[
        "mock",
        "nose",
    ],
    python_requires='>=3.6',
)
