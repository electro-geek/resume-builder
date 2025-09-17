from setuptools import setup

setup(
    name="resume-builder-cli",
    version="1.0.0",
    py_modules=["resume_builder"],
    install_requires=[
        "Jinja2",
    ],
    entry_points={
        "console_scripts": [
            "resume-builder=resume_builder:main",
        ],
    },
)