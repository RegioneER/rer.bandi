# -*- coding: utf-8 -*-


from lxml.builder import E
import lxml.etree
import os

try:
    from zope.app.schema.vocabulary import IVocabularyFactory
except ImportError:
    from zope.schema.interfaces import IVocabularyFactory

from zope.interface.declarations import implements
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm


class ConfigurationError(Exception):
    pass


class XMLFileVocabulary(object):
    """
    Retrieves a vocabulary by reading an XML file on the filesystem.
    """
    implements( IVocabularyFactory )


    def __init__(self, envvar, vocabulary_name, default_terms=None):
        """
        envvar:
            environment variable containing the path of the XML file
        vocabulary_name:
            name attribute of the <vocabulary> element
            (for instance, the name of the vocabulary utility as registered in ZCML)
        """

        if envvar not in os.environ:
            raise ConfigurationError("Missing environment variable %s" % envvar)

        filename = os.environ[envvar]

        if not os.path.exists(filename):
            fout = open(filename, 'wb')
            fout.write(self.default_file_contents(vocabulary_name, default_terms))
            fout.close()
            raise ConfigurationError("Vocabulary file file %s created with default values. Please check the contents and run again." % filename)

        fin = open(filename, 'rb')

        try:
            xml = lxml.etree.parse(fin)
        except lxml.etree.XMLSyntaxError, e:
            raise ConfigurationError("Invalid XML in file %s: %s" % (fin.name, e))

        fin.close()
        self.terms = self.extract_terms(xml, vocabulary_name)


    def extract_terms(self, xml, vocabulary_name):
        terms = []
        for el_term in xml.getroot().xpath("//vocabulary[@name='%s']/term" % vocabulary_name):
            token = el_term.attrib['token']
            try:
                value = el_term.attrib['value']
            except KeyError:
                value = token
            title = el_term.text.strip()
            terms.append(SimpleTerm(token=token, value=value, title=title))
        return sorted(terms, key=lambda x: x.title)


    def __call__(self, context):
        return SimpleVocabulary(self.terms)


    def default_file_contents(self, vocabulary_name, default_terms):
        voc = E('vocabulary', name=vocabulary_name)
        for token, title in default_terms:
            voc.append(E('term', title, token=token))
        root = E('vocab-list')
        root.append(voc)

        xmlbytes = lxml.etree.tostring(root, xml_declaration=True, encoding='utf-8', pretty_print=True)

        return xmlbytes
