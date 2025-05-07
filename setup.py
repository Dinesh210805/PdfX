"""
Setup script for the PdfX package
"""
from setuptools import setup, find_packages
import os

# Read the contents of README file
with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="pdfx",
    version="0.1.0",
    author="PdfX Team",
    author_email="your-email@example.com",
    description="A powerful PDF converter for multiple file types",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/pdfx",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "fpdf",
        "Pillow",
        "python-docx",
        "reportlab",
        "PyPDF2",
        "pdfkit",
        "colorama",
        "tabulate",
        "comtypes;platform_system=='Windows'",
    ],
    entry_points={
        "console_scripts": [
            "pdfx=pdfx.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Utilities",
        "Topic :: Office/Business",
        "Topic :: Multimedia :: Graphics :: Viewers",
    ],
    python_requires=">=3.6",
)
