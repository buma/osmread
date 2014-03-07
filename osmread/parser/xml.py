from lxml.etree import iterparse
from datetime import datetime

from osmread.parser import Parser
from osmread.elements import Node, Way, Relation, RelationMember, TYPE_WAY, TYPE_NODE, TYPE_RELATION


class XmlParser(Parser):

    def __init__(self, **kwargs):
        Parser.__init__(self, **kwargs)
        self._compression = kwargs.get('compression', None)

    def parse(self, fp):
        context = iterparse(fp, events=('start', 'end'))

        # common
        _type = None
        _id = None
        _tags = None
        # node only
        _lon = None
        _lat = None
        # way only
        _nodes = None
        # relation only
        _members = None

        for event, elem in context:

            if event == 'start':
                attrs = elem.attrib
                if elem.tag in ('node', 'way', 'relation'):
                    _id = long(attrs['id'])
                    _tags = {}

                    if elem.tag == 'node':
                        _type = Node
                        _lon = float(attrs['lon'])
                        _lat = float(attrs['lat'])
                    elif elem.tag == 'way':
                        _type = Way
                        _nodes = []
                    elif elem.tag == 'relation':
                        _type = Relation
                        _members = []

                elif elem.tag == 'tag':
                    _tags[unicode(attrs['k'])] = unicode(attrs['v'])

                elif elem.tag == 'nd':
                    _nodes.append(long(attrs['ref']))

                elif elem.tag == 'member':
                    _members.append(
                        RelationMember(
                            unicode(attrs['role']),
                            {
                                'node': TYPE_NODE,
                                'way': TYPE_WAY,
                                'relation': TYPE_RELATION
                            }[attrs['type']],
                            long(attrs['ref'])
                        )
                    )

            elif event == 'end':
                if elem.tag in ('node', 'way', 'relation'):
                    args = [
                        _id,
                        _tags
                    ]

                    if elem.tag == 'node':
                        args.extend((_lon, _lat))

                    elif elem.tag == 'way':
                        args.append(tuple(_nodes))

                    elif elem.tag == 'relation':
                        args.append(tuple(_members))

                    elem.clear()

                    yield _type(*args)
