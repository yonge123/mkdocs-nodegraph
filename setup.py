from setuptools import setup, find_packages

with open('README.md', 'r') as fin:
    long_description = fin.read()

setup(
    name="mkdocs-nodegraph",
    version="0.1.2",
    author="JeongYong Hwang",
    author_email="yonge123@gmail.com",
    keywords=["mkdocs", "plugin", "nodegraph"],
    url="",
    packages=find_packages(),
    license="MIT",
    license_files=["LICENSE"],
    install_requires=[
        "mkdocs>=1.4.0",
        "mkdocs-material>=9.5.31",
        "pyembed-markdown>=1.1.0",
        "mkdocs-glightbox>=0.4.0",
        "pyvis>=0.3.0",
        "PyYAML>=6.0.2",
    ],
    entry_points={
        'mkdocs.plugins': [
            'nodegraph = mkdocs_nodegraph.plugin:GraphViewPlugin',
        ]
    },
    package_data={
        "mkdocs_nodegraph": [
            "nodegraph/graph_opts.json",
            "nodegraph/pyvis_opts.js",
            "nodegraph/templates/__init__.py",
            "nodegraph/templates/template.html",
        ],
    },
    description="Node Graph plugin for Mkdocs Material",
    long_description=long_description,
    long_description_content_type="text/markdown",
)   