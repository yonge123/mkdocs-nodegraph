import os
import subprocess
import mkdocs_nodegraph.nodegraph.generate_graph as generate_graph


def main():
    current_dir = os.path.dirname(__file__)
    docs_dir = os.path.join(current_dir, "examples/docs")
    graph_opts = os.path.join(current_dir, "mkdocs_nodegraph/nodegraph/graph_opts.json")
    pyvis_opts = os.path.join(current_dir, "mkdocs_nodegraph/nodegraph/pyvis_opts.js")

    site_dir = os.path.join(current_dir, "examples/site")
    index_path = os.path.join(site_dir, 'index.html')
    graph_max_html = os.path.join(site_dir, 'nodegraph_max.html')
    graph_html = os.path.join(site_dir, 'nodegraph.html')
    graph_filename = 'nodegraph.html'
    try: 
        cmd = '''cd examples && mkdocs build && cd ..'''
        py2output = subprocess.check_output(cmd, shell=True)
        if py2output:
            py2output = py2output.decode('utf-8')
            print(py2output)
    except Exception as e:
        print(e)
        pass
    else:
        # run after mkdocs build
        generate_graph.build_graph(docs_dir, site_dir, graph_max_html, pyvis_opts, graph_opts, graph_filename)
        generate_graph.rebuild_graph_html(index_path, graph_max_html, graph_html)
        if os.path.isfile(graph_html):
            os.startfile(graph_html)


if __name__ == '__main__':
    main()
    