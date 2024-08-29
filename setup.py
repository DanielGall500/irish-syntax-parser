from setuptools import setup, find_packages

setup(
    # CLause-based Irish Parser
    name='CLIP', 
    version='0.1.0',  
    description='A Clause Parser for the Irish Language.', 
    author='Daniel Gallagher',  
    author_email='daniel.gallagher.js@gmai.com', 
    url='https://github.com/DanielGall500/irish-complementiser-POS-tagging',  
    packages=find_packages(where='src'), 
    package_dir={'': 'src'}, 
    install_requires=[
        'numpy==1.26.4',
        'pandas==2.2.1',
        'pydantic==2.8.2',
        'pydantic_core==2.20.1',
        'python-dateutil==2.9.0.post0',
        'pytz==2024.1',
        'spacy==3.7.4',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',  # Update as necessary
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',  # Update to the license you're using
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',  # Specify the Python versions you're targeting
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    python_requires='>=3.9',  # Specify the Python versions you want to support
    include_package_data=True,  # Include other files specified in MANIFEST.in (if used)
    zip_safe=False,  # Set to True if you don't use non-Python files
)

