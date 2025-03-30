import os, json
from .mdparser import MdParser
import networkx as nx
from pyvis.network import Network
import copy
import os
import re


beautifulcolors = [
    "#E9967A",
    "#00CED1",
    "#90EE90",
    "#CD5C5C",
    "#FF1493",
    "#32CD32",
    "#FF00FF",
    "#4682B4",
    "#DA70D6",
    "#FFD700",
    "#C71585",
    "#FFDAB9",
    "#20B2AA",
    "#FF69B4",
    "#DAA520",
    "#48D1CC",
    "#F0E68C",
    "#9400D3",
    "#FF7F50",
    "#8B008B",
    "#98FB98",
    "#DDA0DD",
    "#6495ED",
    "#4169E1",
    "#87CEEB",
    "#800080",
    "#FFA500",
    "#8E44AD",
    "#9370DB",
    "#3CB371",
    "#8A2BE2",
    "#66CDAA",
    "#9932CC",
    "#BA55D3",
    "#4ECDC4",
    "#8FBC8F",
    "#5F9EA0",
    "#45B7D1",
    "#FA8072",
    "#00FA9A",
    "#F4A460",
    "#6A5ACD",
    "#D2691E",
    "#7B68EE",
    "#40E0D0",
    "#F08080",
    "#B0C4DE",
    "#FF6B6B",
    "#1E90FF",
    "#FF4500",
    "#FFB6C1",
    "#FFA07A",
    "#87CEFA",
]


def set_edge_color_by_dominant_node(net, nx_graph):
    """
    Color each edge based on the color of its most connected node
    """
    # assign node color to font colorS
    for node_id in nx_graph.nodes():
        degree = nx_graph.degree(node_id)
        color = net.get_node(node_id)['color']
        net.get_node(node_id)['font']['color'] = color

    # Count connections for each node
    node_connections = {}
    for node in nx_graph.nodes():
        node_connections[node] = len(list(nx_graph.neighbors(node)))
        
    # For each edge, get its linked nodes and color based on the node with more connections
    for i, edge in enumerate(net.edges):
        from_node = edge['from']
        to_node = edge['to']
        
        # Determine which node has more connections
        if node_connections[from_node] >= node_connections[to_node]:
            node_with_more_connections = from_node
        else:
            node_with_more_connections = to_node
        
        # Find this node in the PyVis nodes list to get its color
        for node in net.nodes:
            if node['id'] == node_with_more_connections:
                node_color = node['color']
                break
        
        # Set the edge color
        net.edges[i]['color'] = node_color
        
        
class GraphOptions():
    def __init__(self, width, height, heading, bgcolor, font_color):
        self.width = width
        self.height = height
        self.heading = heading
        self.bgcolor = bgcolor
        self.font_color = font_color


class GraphBuilder():
    def __init__(self, pyvis_opts, graph_opts, graph_out, config_graphfile, docs_dir, site_dir):
        self.pyvis_opts = pyvis_opts  # js variable as raw string
        self.graph_opts = graph_opts  # GraphOptions obj
        self.graph_out = graph_out    # output path for graph as HTML
        self.config_graphfile = config_graphfile
        self.docsdir = docs_dir
        self.site_dir = site_dir
        self.net = Network(width=graph_opts.width, height=graph_opts.height, 
                           heading=graph_opts.heading, bgcolor=graph_opts.bgcolor, 
                           font_color=graph_opts.font_color,
                        #    select_menu=True,
                        #    filter_menu=True
                           )
        template_dir = os.path.dirname(__file__) + "/templates/"
        self.net.set_template_dir(template_dir)
        self.net.set_template = template_dir + "/template.html"
        
        self.net.set_options(self.pyvis_opts)

        # self.net.show_buttons(filter_=['physics', 'nodes', 'links'])
    # build graph from parsed markdown pages
    def build(self, mdfiles):
        nx_graph = nx.Graph()
        edget_info_dic = dict()
        color_list = copy.deepcopy(beautifulcolors)

        data_dic = dict()
        for mdfile in mdfiles:
            if mdfile.uid not in data_dic:
                data_dic[mdfile.uid] = set()

            for link_uid in mdfile.link_uids:
                if link_uid not in data_dic:
                    data_dic[link_uid] = set()
                
                data_dic[mdfile.uid].add(link_uid)
                data_dic[link_uid].add(mdfile.uid)

        config_graphfile = self.config_graphfile.replace("\\", "/") if "\\" in self.config_graphfile else self.config_graphfile
        level_count = config_graphfile.count('/')
        icon_prefix = ""
        if level_count:
            icon_prefix = (level_count*"../")
            
        for mdfile in mdfiles:
            if not color_list:
                color_list = copy.deepcopy(beautifulcolors)

            docsdir = self.docsdir.replace("\\", "/") + "/"
            site_folder_name = os.path.basename(self.site_dir)
            filepath = mdfile.file_path.replace("\\", "/")
            prefix = filepath.replace(docsdir.replace("\\", "/"), "")
            html = prefix.replace(".md", ".html")
            html = icon_prefix + html
            
            icon = ""
            color = ""
            shape="dot"

            metadata = mdfile.metadata
            if metadata:
                if "mdfile_icon" in metadata:
                    #  variable relative path    ../_source/svgs/blender.svg
                    icon = icon_prefix + metadata["mdfile_icon"]
                if "mdfile_color" in metadata:
                    color = metadata["mdfile_color"]
                    
            if icon:
                shape="image"
                
            if not color:
                color = color_list.pop(0)
            count_links = len(mdfile.link_uids)
            if count_links <= 1:
                color = "#9CA3AF"
                
            size = 50 + (count_links * 4)
            if size > 120:
                size = 120
            nx_graph.add_node(mdfile.uid, 
                            label=mdfile.title, 
                            url=html, 
                            size=size, 
                            shape=shape, 
                            image=icon, 
                            color=color, 
                            opacity=1,
                            borderWidth=2,
                            )
            
            for idx, link_uid in enumerate(mdfile.link_uids):
                if mdfile.uid in data_dic:
                    max_link = len(data_dic[mdfile.uid])
                    if link_uid in data_dic:
                        if max_link < len(data_dic[link_uid]):
                            max_link = len(data_dic[link_uid])
                    edge_len = max_link * 45 + ( idx * 35)
                    nx_graph.add_edge(mdfile.uid, link_uid, length=edge_len)

        # self.net.from_nx(nx_graph) 
        self.net.from_nx(nx_graph, 
                         default_node_size=50, 
                         default_edge_weight=12)
        
        # assign node color to font colorS
        for node_id in nx_graph.nodes():
            degree = nx_graph.degree(node_id)
            color = self.net.get_node(node_id)['color']
            self.net.get_node(node_id)['font']['color'] = color

        set_edge_color_by_dominant_node(self.net, nx_graph)
        
        # save network graph as HTML
        self.net.save_graph(self.graph_out)


def read_config(file_path):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        raise IOError(f'Failed to read file -> "{file_path}"')


def load_graph_opts(config):
    return GraphOptions(config['width'], config['height'], config['heading'],
                        config['bgcolor'], config['font_color'] )


def load_pyvis_opts(file_path):
    with open(file_path, 'r') as fout:
        return fout.read()


def build_graph(docs_dir, site_dir, output_file, pyvis_opts_file, graph_opts_file, config_graphfile):
    if not os.path.isfile(pyvis_opts_file):
        raise IOError(f'Failed to find file -> "{pyvis_opts_file}"')

    if not os.path.isfile(graph_opts_file):
        raise IOError(f'Failed to find file -> "{graph_opts_file}"')

    outputDir = os.path.dirname(output_file)
    os.makedirs(outputDir, exist_ok=True)

    parser = MdParser(docs_dir)
    mdfiles = parser.parse()

    graph_config = read_config(graph_opts_file)
    graph_opts = load_graph_opts(graph_config)
    pyvis_opts = load_pyvis_opts(pyvis_opts_file)
    
    builder = GraphBuilder(pyvis_opts, graph_opts, output_file, config_graphfile, docs_dir, site_dir)
    builder.build(mdfiles)


def rebuild_graph_html(index_path, graph_path, output_path=None):
    """
    Extracts head and body content from graph.html and replaces the content
    of the article tag with class 'md-content__inner md-typeset' in index.html.
    Also adds a custom script at the end of the body.
    
    Args:
        index_path (str): Path to index.html file
        graph_path (str): Path to graph.html file
        output_path (str, optional): Path to save the merged file. If None, overwrites index.html
    """
    # Read the HTML files
    with open(index_path, 'r', encoding='utf-8') as f:
        index_content = f.read()
    
    with open(graph_path, 'r', encoding='utf-8') as f:
        graph_content = f.read()
    
    # Find and extract article content
    article_pattern = r'<article class="md-content__inner md-typeset">.*?</article>'
    article_match = re.search(article_pattern, index_content, re.DOTALL)
    
    if not article_match:
        raise ValueError("Could not find article with class 'md-content__inner md-typeset' in index.html")
    
    # Extract head and body from graph_content
    head_content = ""
    body_content = ""
    
    head_match = re.search(r'<head>.*?</head>', graph_content, re.DOTALL)
    if head_match:
        head_content = head_match.group(0)
        
    body_match = re.search(r'<body>.*?</body>', graph_content, re.DOTALL)
    if body_match:
        body_content = body_match.group(0)
    
    # Create new article content
    new_article_content = f'<article class="md-content__inner md-typeset">{head_content}{body_content}</article>'
    
    # Replace the article content
    modified_content = index_content.replace(article_match.group(0), new_article_content)
    
    # Define the custom script to add at the end of the body
    custom_script = """
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
    
    # Add script before closing body tag
    modified_content = modified_content.replace('</body>', f'{custom_script}</body>')
    
    # Save the merged HTML
    if output_path is None:
        output_path = index_path
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(modified_content)
    
    print(f"Successfully replaced article content in {index_path} with content from {graph_path}, added custom script, and saved to {output_path}")
