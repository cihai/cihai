"""
From bitprophet/releases (BSD 2-clause)

https://github.com/bitprophet/releases/blob/35157fa/releases/__init__.py

Also looking at: https://github.com/bitprophet/releases/blob/master/releases/util.py

Todo / Ideas
------------
Create a separate sphinx extension. Integrate patterns to read through text items
and find #23 and replace with a node reference. Look at nodes.reference automatic
linking. The plus sign is this formatting is automated, customizable via powerful
regular expressions (without needing to deal with boilerplate of writing roles).
"""
import re

from docutils import nodes

year_arg_re = re.compile(r'^(.+?)\s*(?<!\x00)<(.*?)>$', re.DOTALL)


def release_nodes(text, slug, date, config):
    uri = None
    if config.releases_release_uri:
        # TODO: % vs .format()
        uri = config.releases_release_uri % slug
    elif config.releases_github_path:
        uri = "https://github.com/{}/tree/{}".format(config.releases_github_path, slug)

    # Only construct link tag if user actually configured release URIs somehow
    if uri:
        link = '<a class="reference external" href="{}">{}</a>'.format(uri, text)
    else:
        link = text
    datespan = ''
    if date:
        datespan = ' <span style="font-size: 75%;">{}</span>'.format(date)
    header = '<h2 style="margin-bottom: 0.3em;">{}{}</h2>'.format(link, datespan)
    return nodes.section(
        '', nodes.raw(rawtext='', text=header, format='html'), ids=[text]
    )


class TitleVisitor(nodes.NodeVisitor):
    """Look for and link RST that looks like:

    .. raw::

       0.10.1 <2017-09-08>
       -------------------
    """

    def __init__(self, document, app):
        nodes.NodeVisitor.__init__(self, document)
        self.app = app

    def visit_title(self, node):
        text = str(node.astext())
        match = year_arg_re.match(text)

        if match:
            number, date = match.group(1), match.group(2)

            node.parent.replace_self(
                [release_nodes(number, number, date, self.app.config), node.parent[1]]
            )

    def unknown_visit(self, node):
        pass


def parse_changelog(app, doctree):
    # Don't scan/mutate documents that don't match the configured document name
    # (which by default is ['changelog.rst', ]).
    if app.env.docname not in app.config.releases_document_name:
        return

    # Find the first bullet-list node & replace it with our organized/parsed
    # elements.
    changelog_visitor = TitleVisitor(doctree, app)
    doctree.walk(changelog_visitor)


def setup(app):
    for key, default in (
        # Issue base URI setting: releases_issue_uri
        # E.g. 'https://github.com/fabric/fabric/issues/'
        ('issue_uri', None),
        # Release-tag base URI setting: releases_release_uri
        # E.g. 'https://github.com/fabric/fabric/tree/'
        ('release_uri', None),
        # Convenience Github version of above
        ('github_path', None),
        # Which document to use as the changelog
        ('document_name', ['changelog']),
    ):
        app.add_config_value(
            name='releases_{}'.format(key), default=default, rebuild='html'
        )

    app.connect('doctree-read', parse_changelog)
