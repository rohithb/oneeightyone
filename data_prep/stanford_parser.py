
import os
import tempfile
from nltk.parse.api import ParserI


class StanfordParser(ParserI):

    def __init__(self, working_dir=None,
                 output_format="typedDependencies",
                 model="englishPCFG"):
        """
        An interface for parsing with the Stanford Parser.
        :param working_dir: Absolute path to the Stanford
        parser without trailing slash should be given
        :param output_format :
        """
        if(working_dir is None):
            self.working_dir = '/usr/lib/stanford-parser-*'
        else:
            self.working_dir = working_dir
        self.output_format = output_format
        self.model = model

    def parse(self, text):
        """
        Use Stanford parser for dependency parsing a text consisting of
        many sentences.
        The parser will automatically separate sentences and create
        typed dependency for each sentence separately.

        :param text: Input text to parse
        :type text: string
        :return:`Typed dependency relation` of the sentences in the input text
        """
        in_file = self.makeFile(text)
        cmd = ('java -mx512m -cp "' + self.working_dir + '/*:"'
               ' edu.stanford.nlp.parser.lexparser.LexicalizedParser'
               ' -outputFormat ' + self.output_format +
               ' edu/stanford/nlp/models/lexparser/' + self.model + '.ser.gz '
               + in_file + ' >' + self.working_dir + '/stanford_output.txt')
        os.system(cmd)
        out_file = open(self.working_dir + "/stanford_output.txt")
        ret = out_file.read()
        os.remove(self.working_dir + '/stanford_output.txt')
        os.remove(in_file)
        return ret

    def makeFile(self, text):
        """
        This method will copy the input text into a temporary file

        :param text: Input text to parse
        :type sentence: string
        :return: name of temporary file containing the input text.
        """
        input_file = tempfile.NamedTemporaryFile(prefix='stanford_input.txt',
                                                 dir=self.working_dir,
                                                 delete=False)
        input_file.file.write(bytes(text, 'utf-8'))
        input_file.file.write(bytes('\n','utf-8'))
        return input_file.name
