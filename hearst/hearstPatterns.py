import re
import nltk
from nltk.tag.perceptron import PerceptronTagger

class HearstPatterns(object):

    def __init__(self, extended=False):
        self.__chunk_patterns = r""" #  helps us find noun phrase chunks
                NP: {<DT>?<JJ.*>*<NN.*>+}
                    {<NN.*>+}
                """
        # create a chunk parser
        self.__np_chunker = nltk.RegexpParser(self.__chunk_patterns)

        # now define the Hearst patterns
        # format is <hearst-pattern>, <hypernym_location>
        # so, what this means is that if you apply the first pattern,

        self.__hearst_patterns = [
            (
                "(NP_\w+ (, )?such as (NP_\w+ ?(, )?(and |or )?)+)",
                "first"
            ),
            (
                "(such NP_\w+ (, )?as (NP_\w+ ?(, )?(and |or )?)+)",
                "first"
            ),
            (
                "((NP_\w+ ?(, )?)+(and |or )?other NP_\w+)",
                "last"
            ),
            (
                "(NP_\w+ (, )?including (NP_\w+ ?(, )?(and |or )?)+)",
                "first"
            ),
            (
                "(NP_\w+ (, )?especially (NP_\w+ ?(, )?(and |or )?)+)",
                "first"
            ),
        ]

        if extended:
            self.__hearst_patterns.extend([
                (
                    "((NP_\w+ ?(, )?)+(and |or )(any |some )other NP_\w+)",
                    "last"
                ),
                (
                    "((NP_\w+ ?(, )?(and |or )?)+are a NP_\w)",
                    "last"
                ),
                (
                    "(NP_\w+ (, )?which include (NP_\w+ ?(, )?(and |or )?)+)",
                    "first"
                ),
                (
                    "((NP_\w+ ?(, )?(and |or )?)+(are |is |was |were )(a |an )NP_\w)",
                    "last"
                ),
                # (
                #     "(NP_\w+ (, )?like (NP_\w+ ? (, )?(and |or )?)+)",
                #     "first"
                # ),
                # (
                #     "((NP_\w+ ?(, )?)+(and |or )one of (the |these |those )NP_\w+)",
                #     "last"
                # ),
                (
                    "(examples? of NP_\w+ (, )?(is |are )(NP_\w+ ?(, )?(and |or )?)+)",
                    "first"
                ),
                (
                    "((NP_\w+ ?(, )?(and |or )?)+(are |is )examples? of NP_\w+)",
                    "last"
                ),
                (
                    "(NP_\w+ (, )?for example (, )?(NP_\w+ ?(, )?(and |or )?)+)",
                    "first"
                ),
                (
                    "((NP_\w+ ?(, )?(and |or )?)+which (is |are )called NP_\w+)",
                    "last"
                ),
                (
                    "((NP_\w+ ?(, )?(and |or )?)+which (is a|are )NP_\w)",
                    "last",
                ),
                # (
                #     "(NP_\w+ (, )?(mainly |mostly |notably |particularly |principally )(NP_\w+ ? (, )?(and |or )?)+)",
                #     "first"
                # ),
                # (
                #     "(NP_\w+ (, )?in particular (NP_\w+ ?(, )?(and |or )?)+)",
                #     "first"
                # ),
                # (
                #     "(NP_\w+ (, )?except (NP_\w+ ?(, )?(and |or )?)+)",
                #     "first"
                # ),
                (
                    "(NP_\w+ (, )?other than (NP_\w+ ?(, )?(and |or )?)+)",
                    "first"
                ),
                # (
                #     "(NP_\w+ (, )?(e.g. |i.e. )(, )?(NP_\w+ ?(, )?(and |or )?)+)",
                #     "first"
                # ),
                # (
                #     "((NP_\w+ ?(, )?(and |or )?)+, a (kind |form )of NP_\w+)",
                #     "last"
                # ),
                (
                    "((NP_\w+ ?(, )?(and |or )?)+, (kinds |forms )of NP_\w+)",
                    "last"
                ),
                # (
                #     "((NP_\w+ ?(, )?(and |or )?)+which (look |sound )like NP_\w+)",
                #     "last"
                # ),
                # (
                #     "(NP_\w+ (, )?which (are |is )similar to (NP_\w+ ?(, )?(and |or )?)+)",
                #     "first"
                # ),
                # (
                #     "(NP_\w+ (, )?examples? of this (is |are )(NP_\w+ ?(, )?(and |or )?)+)",
                #     "first"
                # ),
                # (
                #     "(NP_\w+ (, )?types (, )?(NP_\w+ ?(, )?(and |or )?)+)",
                #     "first"
                # ),
                # (
                #     "((NP_\w+ ?(, )?(and |or )?)+NP_\w+ types)",
                #     "last"
                # ),
                # (
                #     "(NP_\w+ (, )?whether (NP_\w+ ? (, )?(and |or )?)+)",
                #     "first"
                # ),
                # (
                #     "(compare (NP_\w+ ?(, )?(and |or )?)+with NP_\w+)",
                #     "last"
                # ),
                # (
                #     "(NP_\w+ (, )?compared to (NP_\w+ ? (, )?(and |or )?)+)",
                #     "first"
                # ),
                # (
                #     "(NP_\w+ (, )?among them (NP_\w+ ?(, )?(and |or )?)+)",
                #     "first"
                # ),
                # (
                #     "((NP_\w+ ?(, )?(and |or )?)+as NP_\w+)",
                #     "last"
                # ),
                # (
                #     "(NP_\w+ (, )?(NP_\w+ ?(, )?(and |or )?)+for instance)",
                #     "first"
                # ),
                # (
                #     "((NP_\w+ ?(, )?(and |or )?)+the many NP_\w+)",
                #     "last"
                # ),
                # (
                #     "((NP_\w+ ?(, )?(and|or)?)+sort of NP_\w+)",
                #     "last"
                # ),
                # (
                #     "(NP_\w+ (, )?which (may |can )?include (NP_\w+ ?(, )?(and |or )?)+)",
                #     "first"
                # )
            ])
        self.__pos_tagger = PerceptronTagger()

    def prepare(self, rawtext):
        # To process text in NLTK format
        sentences = nltk.sent_tokenize(rawtext.strip())
        sentences = [nltk.word_tokenize(sent) for sent in sentences]
        sentences = [self.__pos_tagger.tag(sent) for sent in sentences]

        return sentences

    def chunk(self, rawtext):
        sentences = self.prepare(rawtext.strip())

        all_chunks = []
        for sentence in sentences:
            chunks = self.__np_chunker.parse(sentence)
            all_chunks.append(self.prepare_chunks(chunks))

        # two or more NPs next to each other should be merged into a single NP,
        # find any N consecutive NP_ and merge them into one...
        # Eg: "NP_foo NP_bar blah blah" becomes "NP_foo_bar blah blah"
        all_sentences = []
        for raw_sentence in all_chunks:
            sentence = re.sub(r"(NP_\w+ NP_\w+)+",
                              lambda m: m.expand(r'\1').replace(" NP_", "_"),
                              raw_sentence)
            all_sentences.append(sentence)

        return all_sentences

    def prepare_chunks(self, chunks):
        # If chunk is NP, start with NP_ and join tokens in chunk with _
        # Else just keep the token as it is

        terms = []
        for chunk in chunks:
            label = None
            try:
                # gross hack to see if the chunk is simply a word or a NP, as
                # we want. But non-NP fail on this method call
                label = chunk.label()
            except:
                pass

            if label is None:  # means one word...
                token = chunk[0]
                terms.append(token)
            else:
                np = [a[0] for a in chunk if a[1] in ['NN', 'NNS', 'NNP', 'NNPS']]
                np = "NP_" + "_".join(np)
                # np = "NP_"+"_".join([a[0] for a in chunk])
                terms.append(np)
        return ' '.join(terms)

    def find_hyponyms(self, rawtext):

        hypo_hypernyms = []
        np_tagged_sentences = self.chunk(rawtext)

        for sentence in np_tagged_sentences:

            for (hearst_pattern, parser) in self.__hearst_patterns:
                matches = re.search(hearst_pattern, sentence)
                if matches:
                    match_str = matches.group(0)

                    nps = [a for a in match_str.split() if a.startswith("NP_")]

                    if parser == "first":
                        hypernym = nps[0]
                        hyponyms = nps[1:]
                    else:
                        hypernym = nps[-1]
                        hyponyms = nps[:-1]

                    for i in range(len(hyponyms)):
                        hypo_hypernyms.append(
                            (self.clean_hyponym_term(hyponyms[i]),
                             self.clean_hyponym_term(hypernym)))

        return hypo_hypernyms

    def clean_hyponym_term(self, term):
        return term.replace("NP_", "").split("_")[-1]


if __name__=='__main__':
    hp = HearstPatterns(extended=False)
    text = 'I like to listen to music from musical genres such as blues, rock and jazz.'
    hps = hp.find_hyponyms(text)
