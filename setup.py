from setuptools import setup, find_packages

setup(
    name="cold-lead-finder",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "typer==0.12.3",
        "praw==7.7.1",
        "requests==2.31.0",
        "openai==1.12.0",
    ],
    entry_points={
        "console_scripts": [
            "cold-lead-finder=cold_lead_finder.main:app",
        ],
    },
)