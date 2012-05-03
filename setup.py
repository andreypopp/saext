from setuptools import setup, find_packages
import sys, os

version = "0.1"

setup(name="saext",
      version=version,
      description="Various SQLAlchemy utilities",
      author="Andrey Popp",
      author_email="8mayday@gmail.com",
      license="BSD",
      packages=find_packages(exclude=["ez_setup", "examples", "tests"]),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
