#!/usr/bin/python

__version__ = "0.0.2"

import math
import csv
import argparse
from dataclasses import dataclass, field

interactive = 1

@dataclass
class Feature():
    name: str
    freq: float = field(default=float("nan"))

    def __repr__(self):
        return "%-50s  %6.2f" % (self.name, float(self.freq))

@dataclass
class Grave():
    name: str
    features: list = field(default_factory=list)

    def __repr__(self):
        return str(self.name)

@dataclass
class Pair():
    g1: Grave
    g2: Grave
    common: int = 0
    equality: int = 0

    def __repr__(self):
        return "%-25s%-25s %0.2f (%d)" % (self.g1.name, self.g2.name, self.equality, self.common)

def parse_input_feature(f):
    input_format = {
        "-":     -1,
        "1":      1,
        "0":      0,
        "-1":   (-1,  1),
        "1-":   ( 1, -1),
        "0,1":  ( 0,  1),
        "0-1":  ( 0, -1),
        "11":   ( 1,  1),
        "-10":  (-1,  0),
        "10":   ( 1,  0),

        # Next wrongly used:
#        "0.1":  ( 0,  1),
#        "1?":   ( 1,  0),
#
#        "?0":   ( 0,  0),
#        "0?":   ( 0,  0), 
#        "0, ?": ( 0,  0),
#        "-?":   ( 0,  0),
#        "":       0,
#        "C":      0,
    }
    if f not in input_format:
        raise Exception("Neznámý formát znaku: '%s'" % f)
    return input_format[f]

def load_file(filename):
    graves = []
    features = []
    errors = []
    with open(filename, 'r') as csvfile:
        freq_index = None
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')

        row = next(reader)

        # Check for column with name "freq"
        if "freq" in row:
            freq_index = row.index("freq")
            row.pop(freq_index)

        name_index = row.index("name") if "name" in row else 0
        row.pop(name_index)

        # First line contains grave names
        graves += [Grave(x) for x in row]

        for row in reader:
            # Get frequency, if the column exists
            freq = float(row.pop(freq_index).replace(",", ".")) if freq_index != None else float("nan")
            name = row.pop(name_index)
            features += [Feature(name, freq)]

            for grave, val in zip(graves, row):
                try:
                    grave.features += [parse_input_feature(val)]
                except Exception as ex:
                    # Add unknown state of feature
                    grave.features += [0]
                    # Print error info only once
                    if str(ex) not in errors:
                        print("Chyba vstupu:", ex)
                        errors += [str(ex)]
    return (graves, features, errors)

def save_freq(name, features):
    with open("%s_freq.csv" % name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Nazev vlastnosti", "Frekvence [%]"])
        for f in features:
            writer.writerow([f.name, f.freq])

def save_pairs(name, pairs):
    with open("%s_pairs.csv" % output_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Hrob 1", "Hrob 2", "Koeficient pribuznosti", "Pocet shodnych znaku"])
        for p in pairs:
            writer.writerow([p.g1.name, p.g2.name, "%.2f" % p.equality, p.common])

def print_freqs(features, count):
    if count > 0:
        print()
        print("Jmeno vlastnosti                                    Frekvence")
        print("================================================================")
        for f in features[0:count]:
            print(f)

def print_pairs(pairs, count):
    if count > 0:
        print()
        print("%-25s%-25s  %4s (%s)" % ("Hrob 1", "Hrob 2", "Koef", "Pocet"))
        print("================================================================")
        for p in pairs[0:count]:
            print(p)

def compare_feature(f1, f2):
    if type(f1) != type(f2):
        raise Exception("Nesouhlasí typ znaku")

    if type(f1) == int:
        return 1 == f1 == f2
    elif type(f1) == tuple:
        # Alespoň jeden znak je společný
        return True in [1 == x == y for x, y in zip(f1,f2)]

def create_pairs(graves, features):
    errors_f = []
    errors_g = []
    pairs = []
    for g1 in range(len(graves)):
        for g2 in range(g1+1, len(graves)):
            p = Pair(graves[g1], graves[g2])
            pairs += [p]
            for f in range(len(features)):
                f1 = p.g1.features[f]
                f2 = p.g2.features[f]
                try:
                    if compare_feature(f1, f2):
                        p.common += 1
                        p.equality += features[f].freq
                except Exception as e:
                    pass
                    #print("Nesouhlasí typ znaku %s: hrob '%s' má hodnotu '%s', hrob '%s' má hodnotu '%s'" % (features[f].name, p.g1.name, f1, p.g2.name, f2))
                    #if features[f].name not in errors_f:
                    #    errors_f += [features[f].name]
                    #if p.g1.name not in errors_g:
                    #    errors_g += [p.g1.name]
                    #if p.g2.name not in errors_g:
                    #    errors_g += [p.g2.name]

            if p.common > 0:
                p.equality /= p.common
    #print("Tyto vlastnosti obsahovaly chybu:", errors_f)
    #print("Tyto hroby obsahovaly chybu:", errors_g)
    return pairs

def compute_frequency_veleminsky(graves, f):
    positive = 0
    detected = 0
    for g in graves:
        feature = g.features[f]
        if type(feature) == tuple:
            positive += 1 if 1 in feature else 0
            # INFO: nejsou započteni jedinci, u kterých je přítomná pouze jedna strana, pokud na této straně hodnocený znak není.
            detected += 1 if not (0 in feature and -1 in feature) else 0
        elif type(feature) == int:
            positive += 1 if feature == 1 else 0
            detected += 1 if feature != 0 else 0
        else:
            raise Exception("Unknown feature type")
    return positive / detected * 100

def do_work(files):
    features = []
    graves = []

    # FIXME: Currently support for only one file due to indexes
    for filename in files[:1]:
        g, f, e = load_file(filename)
        graves += g
        features += f

    # Compute frequency if not supplied
    for f in range(len(features)):
        if math.isnan(features[f].freq):
            features[f].freq = compute_frequency_veleminsky(graves, f)

    # Go through all grave pairs and check for common features
    pairs = create_pairs(graves, features)

    # Sort pairs by equality
    pairs.sort(key = lambda p : p.equality, reverse = True)
    
    return (features, graves, pairs)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'Zpracuje vlastnosti koster z ruzych hrobu.',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-f', '--freq', help='vypocitat frekvenci', default=False, action='store_true', dest='force_freq')
    parser.add_argument('-m', help='zobrazit maximalne M frekvenci', type=int, dest='count_freqs', default=0)
    parser.add_argument('-n', help='zobrazit maximalne N paru', type=int, dest='count_pairs', default=10)
    parser.add_argument('files', metavar='graves.csv', nargs='*', help='soubor s daty', default=['graves.csv'])
    args = parser.parse_args()

    features, graves, pairs = do_work(args.files)

    print("Pocet vlastnosti                                    %4s" % len(features))
    print("Pocet hrobu                                         %4s" % len(graves))
    print("Pocet paru                                          %4s" % len(pairs))

    output_name = '.'.join(args.files[0].split('.')[:-1])

    save_freq(output_name, features)
    save_pairs(output_name, pairs)

    print_freqs(features, args.count_freqs)
    print_pairs(pairs, args.count_pairs)

    if interactive:
        input(">>> Press Enter <<<")
