from setuptools import setup, find_packages


def get_requirements():
    with open("requirements.txt", "r") as req:
        requires = req.readlines()
    return [req.strip() for req in requires]


setup(
    name='data_diff',
    version='1.0.0',
    description='Data difference',
    url='https://github.com/delatars/data_diff',
    author='Alexander Morokov',
    author_email='morocov.ap.muz@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=get_requirements(),
    entry_points={
        'console_scripts': ['data_diff=data_diff.main:main'],
    }
)