from setuptools import setup, find_packages 

setup(
    name="my_package",
    version="0.1.0",
    author="Your Name",
    description="A sample Python package for math and string utilities",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=["beautifulsoup4", "pandas", "pytest", "wordfreq", "argparse", "matplotlib", "requests"],  # Add dependencies here
)
