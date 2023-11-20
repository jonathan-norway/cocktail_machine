from setuptools import setup, find_packages

setup(name='MixMaster', version='0.1', py_modules=["frontend"], packages=find_packages(), entry_points={
    "console_scripts": [
      'mixmaster = frontend.app:main'
      ]
})
