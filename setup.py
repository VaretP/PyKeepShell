import setuptools

with open('README.md', 'r') as readme:
    long_description = readme.read()

setuptools.setup(
    name="pykeep",
    version="0.0.1",
    packages=['pykeep'],
    entry_points = {
        'console_scripts': [
            'pykeep=pykeep.__main__:main'
        ],
    },
    author="Paul VARET",
    author_email="paul.varet@protonmail.com",
    description="Shell like dotfiles manager and editor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/VaretP/PyKeepShell",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"]
)
