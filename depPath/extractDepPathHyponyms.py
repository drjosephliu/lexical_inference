import os
import pprint
import argparse

pp = pprint.PrettyPrinter()
parser = argparse.ArgumentParser()

parser.add_argument('--wikideppaths', type=str, required=True)
parser.add_argument('--relevantdeppaths', type=str, required=True)
parser.add_argument('--outputfile', type=str, required=True)


def extractHyperHypoExtractions(wikideppaths, relevantPaths):
    '''Each line in wikideppaths contains 3 columns
        col1: word1
        col2: word2
        col3: deppath
    '''

    # Should finally contain a list of (hyponym, hypernym) tuples
    depPathExtractions = []

    '''
        IMPLEMENT
    '''

    with open(wikideppaths, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            word1, word2, deppath = line.split("\t")

            if deppath in relevantPaths:
                if relevantPaths[deppath] == "forward":
                    depPathExtractions.append((word1, word2))
                elif relevantPaths[deppath] == "reverse":
                    depPathExtractions.append((word2, word1))


    return depPathExtractions


def readPaths(relevantdeppaths):
    '''
        READ THE RELEVANT DEPENDENCY PATHS HERE
    '''
    # Key is deppath,
    # Value is "forward", "backward" or "negative"
    relevantPaths = {}

    with open(relevantdeppaths, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            dep_path, path_type = line.split("\t")
            relevantPaths[dep_path] = path_type

    return relevantPaths


def writeHypoHyperPairsToFile(hypo_hyper_pairs, outputfile):
    directory = os.path.dirname(outputfile)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(outputfile, 'w') as f:
        for (hypo, hyper) in hypo_hyper_pairs:
            f.write(hypo + "\t" + hyper + '\n')


def main(args):
    print(args.wikideppaths)

    relevantPaths = readPaths(args.relevantdeppaths)

    hypo_hyper_pairs = extractHyperHypoExtractions(args.wikideppaths,
                                                   relevantPaths)

    writeHypoHyperPairsToFile(hypo_hyper_pairs, args.outputfile)


if __name__ == '__main__':
    args = parser.parse_args()
    pp.pprint(args)
    main(args)
