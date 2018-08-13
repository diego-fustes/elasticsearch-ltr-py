from elasticsearch import Elasticsearch
from elasticsearch.client import Transport
from .ltr import LTRClient


class ElasticsearhLTR(Elasticsearch):

    def __init__(self, hosts=None, transport_class=Transport, **kwargs):
        """
            :arg hosts: list of nodes we should connect to. Node should be a
                dictionary ({"host": "localhost", "port": 9200}), the entire dictionary
                will be passed to the :class:`~elasticsearch.Connection` class as
                kwargs, or a string in the format of ``host[:port]`` which will be
                translated to a dictionary automatically.  If no value is given the
                :class:`~elasticsearch.Urllib3HttpConnection` class defaults will be used.

            :arg transport_class: :class:`~elasticsearch.Transport` subclass to use.

            :arg kwargs: any additional arguments will be passed on to the
                :class:`~elasticsearch.Transport` class and, subsequently, to the
                :class:`~elasticsearch.Connection` instances.


        """
        Elasticsearch.__init__(self, hosts=hosts, transport_class=transport_class, **kwargs)

        self.ltr = LTRClient(self)
