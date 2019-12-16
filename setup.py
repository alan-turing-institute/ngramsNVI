from setuptools import find_packages, setup

with open('requirements.txt') as f:
    reqs = f.read().splitlines()

setup(
    name='ngramsNVI',
    version='v0.1',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=[],
    tests_require=["pytest"],
    url='https://github.com/alan-turing-institute/ngramsNVI.git',
    license='',
    author='Chanuki Seresinhe',
    author_email='cseresinhe@turing.ac.uk',
    description='Code to be able to create a National Valence Index using Google ngrams data and affective word norms data'
)
