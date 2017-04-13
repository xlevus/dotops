from setuptools import setup, find_packages

setup(
    name="dotops",
    version="0.0-prototype",
    author="Chris Targett",
    url='https://github.com/xlevus/dotops',
    packages=find_packages(exclude=['tests', 'example', 'docs']),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.5,'],
    install_requires=[
        "hy",
        "plumbum"],
    entry_points={
        'console_scripts': [
            'dotops=dotops.command:main',
            'dotops-exec=dotops.modules.command:exec',
            'dotops-apply=dotops.recipes.command:apply']})
