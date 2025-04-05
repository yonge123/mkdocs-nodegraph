import logging
import os
import re
from mkdocs.config.config_options import Type
import mkdocs.plugins
from .nodegraph import generate_graph


log = logging.getLogger(__name__)
base_path = os.path.dirname(os.path.abspath(__file__))


class GraphViewPlugin(mkdocs.plugins.BasePlugin):
    config_scheme = (
        ('graphfile', Type(str, default='nodegraph.html')),
    )
    
    def get_config_graphfile(self):
        graphfile = self.config['graphfile']
        graphfile = graphfile.replace('\\', '/')
        rgx = re.search(r'\w.+', graphfile)
        if rgx:
            return rgx.group()
        else:
            return graphfile

    def on_post_page(self, output, page, config):
        dest_path  = page.file.dest_path
        dest_path = dest_path.replace("/", "\\") if "/" in dest_path else dest_path
        level_count = dest_path.count('\\')
        prefix = ""
        if level_count:
            prefix = (level_count*"../")
        graphfile = prefix + self.get_config_graphfile()
        my_html = f'''<form class="md-header__option" data-md-component="palette">
        <a href="{graphfile}" class="md-header__button md-graph" data-md-component="logo">
            <svg class="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" viewBox="0 0 24 24">
                <path d="M17.5 3a3.5 3.5 0 0 0-3.456 4.06L8.143 9.704a3.5 3.5 0 1 0-.01 4.6l5.91 2.65a3.5 3.5 0 1 0 .863-1.805l-5.94-2.662a3.53 3.53 0 0 0 .002-.961l5.948-2.667A3.5 3.5 0 1 0 17.5 3Z"/>
            </svg>
        </a>
        '''
        output = output.replace('<form class="md-header__option" data-md-component="palette">', my_html)
        
        html_filename = page.file.name
        graphfile_basename = os.path.basename(graphfile)
        graphfilename = graphfile_basename.rsplit('.', 1)[0] if '.' in graphfile_basename else graphfile_basename
        if html_filename == graphfilename:
            script = """
                <script>
                    document.addEventListener('DOMContentLoaded', function() {
                        const footerMetas = document.querySelectorAll('.md-footer-meta.md-typeset');
                        footerMetas.forEach(function(element) {
                            element.remove();
                        });
                        
                        document.querySelector('.md-typeset').style.fontSize = '0px';
                        document.querySelector('.md-typeset').style.margin = '0px';
                    });

                    var right_sidebar = document.getElementsByClassName('md-sidebar md-sidebar--secondary');
                    if (right_sidebar.length > 0) {
                        right_sidebar[0].style.width = '0px';
                    }
                    
                </script>
                """
            # Insert the script before the closing </body> tag
            output = output.replace('</body>', f'{script} </body>')
                
        return output
        
    def on_post_build(self, config, **kwargs):
        docs_dir = config["docs_dir"]
        site_dir = config['site_dir']
        config_graphfile = self.get_config_graphfile()
        if not config_graphfile.endswith(".html"):
            config_graphfile = config_graphfile + ".html"
        graph_html = os.path.join(site_dir, config_graphfile)
        graph_max_html = os.path.join(site_dir, config_graphfile.replace(".html", "_max.html"))
        graph_opts_file = os.path.join(os.path.dirname(__file__), "nodegraph/graph_opts.json")
        pyvis_opts_file = os.path.join(os.path.dirname(__file__), "nodegraph/pyvis_opts.js")

        if os.path.isfile(graph_max_html):
            os.remove(graph_max_html)
        generate_graph.build_graph(docs_dir, site_dir, graph_max_html, pyvis_opts_file, graph_opts_file, config_graphfile)

        index_html = os.path.join(site_dir, 'index.html')
        generate_graph.rebuild_graph_html(index_html, graph_max_html, graph_html)
        