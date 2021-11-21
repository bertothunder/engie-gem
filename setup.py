import json
from setuptools import setup


with open("requirements.txt") as f:
    required = f.read().splitlines()


with open("manifest.json", "r") as f:
    manifest = json.load(f)


setup(
    name="engie-gem-spaas",
    version=manifest["version"],
    packages=[
        "app",
        "app.core",
        "app.services",
    ],
    include_package_data=True,
    zip_safe=False,
    package_data={"config": ["config/*.json"], "": ["alembic.ini"]},
    author="Alberto Curro",
    author_email="bertothunder@gmail.com",
    install_requires=[
        required,
    ],
    entry_points="""
        [console_scripts]
            api = main:main
    """,
)
