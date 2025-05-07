"""
Setup script for the PdfIt package
"""
from setuptools import setup, find_packages
import os

# Read the contents of README file
with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="pdfit",
    version="0.1.0",
    author="PdfIt Team",
    author_email="dinesh@example.com", 
    description="A powerful PDF converter for multiple file types",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Dinesh210805/pdfit",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "fpdf>=1.7.2",
        "Pillow>=10.0.0",
        "python-docx>=0.8.11",
        "reportlab>=3.6.13",
        "PyPDF2>=3.0.0",
        "pdfkit>=1.0.0",
        "colorama>=0.4.6",
        "tabulate>=0.9.0",
        "comtypes>=1.1.14;platform_system=='Windows'",
        "docx2pdf>=0.1.8",
    ],
    entry_points={
        "console_scripts": [
            "pdfit=pdfit.cli:run_pdfit",
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
    ],    python_requires=">=3.6",
    extras_require={
        "html": ["wkhtmltopdf-binary>=0.12.6"],  # Optional package for HTML conversion
    },
    package_data={
        "pdfx": ["README.md"],
    },
)
