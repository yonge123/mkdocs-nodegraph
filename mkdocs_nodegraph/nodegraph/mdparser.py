import os, re, yaml
from .mdfile import MdFile

INLINE_LINK_RE = re.compile(r'\[([^\]]+)\]\(([^)]+\.md)\)')
FOOTNOTE_LINK_TEXT_RE = re.compile(r'\[([^\]]+)\]\[(\d+)\]')
FOOTNOTE_LINK_URL_RE = re.compile(r'\[(\d+)\]:\s+(\S+)')


def find_md_links(md):
    """ Return dict of links in markdown """
    links = dict(INLINE_LINK_RE.findall(md))
    footnote_links = dict(FOOTNOTE_LINK_TEXT_RE.findall(md))
    footnote_urls = dict(FOOTNOTE_LINK_URL_RE.findall(md))

    for key, value in footnote_links.items():
        footnote_links[key] = footnote_urls[value]
    links.update(footnote_links)

    return links


def iterMarkdownLink(mdfile):
    with open(mdfile, 'r', encoding="UTF-8") as fin:
        read = fin.read()
        links = find_md_links(read)
        for label, url in links.items():
            yield url


def getMetadata(mdfile):
    metadata = ""
    count = 0
    with open(mdfile, 'r', encoding="UTF-8") as fin:
        for line in fin.readlines():
            
            if count >= 2:
                break
            
            if line.strip().startswith('#'):
                break
            
            if line.strip() == "---":
                count += 1
            else:
                if count >= 1:
                    metadata += line
    
    return metadata


class MdParser():

    def __init__(self, target_dir):
        self.mdfiles = []
        self.target_dir = target_dir

    def parse_md(self, file_name):
        base_name = os.path.basename(file_name)
        links = list(iterMarkdownLink(file_name))
        link_uids = list()
        title = ""
        metadata = ""
        return MdFile(file_name, base_name, title, links, link_uids, metadata)

    def parse(self):
        uid = 1
        for subdir, dirs, files in os.walk(self.target_dir):
            for f in files:
                if f.endswith('md'):
                    path = os.path.join(subdir, f)

                    if not any(x for x in self.mdfiles if x.file_path == path):
                        md = self.parse_md(path)
                        parseMedata = getMetadata(path)
                        if parseMedata:
                            metadata = yaml.safe_load(parseMedata)
                            md.metadata = metadata
                            
                        md.uid = uid
                        uid += 1
                        self.mdfiles.append(md)

        for mdfile in self.mdfiles:
            uids = set()
            
            for link in mdfile.mdlinks:
                link_basename = os.path.basename(link)
                link_new = link.replace("../", "/").replace("./", "").replace("/", "").replace(".", "")
                uid = list(filter(lambda x: (x.file_path.replace("\\", "").replace("../", "/").replace("./", "").replace("/", "").replace(".", "").endswith(link_new) and os.path.basename(x.file_path) == link_basename), self.mdfiles))
                if len(uid) > 0:
                    uids.add(uid[0].uid)
                    
            mdfile.link_uids = list(uids)
            
        return self.mdfiles
