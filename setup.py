from setuptools import find_packages, setup

setup(
    name="movie_context",
    version='0.0.1',
    description='finds contexts for movie quotes',
    # long_description=long_description,
    url='https://github.com/benhoff/blog',
    license='GPL3',
    classifiers=[
        'Development Status :: 1 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent'],
    author='Ben Hoff',
    author_email='beohoff@gmail.com',
    packages=find_packages(), # exclude=['docs', 'tests']

    install_requires=[
        'praw',
        'python-Levenshtein',
        ],

    extras_require={
        'dev': ['flake8', 'twine'],
    }
)
