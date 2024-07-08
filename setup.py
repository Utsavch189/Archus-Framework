from setuptools import setup, find_packages

with open("./README.md", "r") as f:
    long_description = f.read()

setup(
    name='archus',
    version='1.1.0',
    # package_dir={"": "archus"},
    # packages=find_packages(where="archus"),
    long_description=long_description ,
    long_description_content_type="text/markdown",
    url="https://github.com/Utsavch189/Archus-Framework",
    author="Utsav Chatterjee",
    author_email="utsavchatterjee71@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'Jinja2', 'waitress', 'gunicorn'
    ],
    entry_points={
        'console_scripts': [
            'archus=archus.cli:main',
        ],
    },
    python_requires=">=3.10",
)
