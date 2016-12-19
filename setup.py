from distutils.core import setup
import py2exe

setup(
    console=["facebook_scraper.py"],
    zipfile = None,
    options={
        "py2exe":{
            "optimize": 2
        }
    }   
)
