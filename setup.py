from setuptools import setup, find_packages

with open('README.md', 'r') as fin:
    long_description = fin.read()

setup(
    name="mkdocs-nodegraph",
    version="0.2.0",
    description="Node Graph plugin for Mkdocs Material",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="JeongYong Hwang",
    author_email="yonge123@gmail.com",
    keywords=["mkdocs", "plugin", "nodegraph"],
    url="https://yonge123.github.io/mkdocs-nodegraph/nodegraph.html",
    project_urls={
        "Source": "https://github.com/yonge123/mkdocs-nodegraph/tree/master",
        "Bug Tracker": "https://github.com/yonge123/mkdocs-nodegraph/issues",
        "Documentation": "https://github.com/yonge123/mkdocs-nodegraph/tree/master",
    },
    license="MIT",
    license_files=["LICENSE"],
    packages=find_packages(),
    install_requires=[
        "mkdocs>=1.4.0",
        "mkdocs-material>=9.5.31",
        "pyembed-markdown>=1.1.0",
        "mkdocs-glightbox>=0.4.0",
        "pyvis>=0.3.0",
        "PyYAML>=6.0.2",
    ],
    python_requires='>=3.9',
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
)   