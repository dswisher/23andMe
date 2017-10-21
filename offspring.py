
import sys


def parse(fp):
    line = fp.readline().strip()
    if line == "":
        return None
    if line[:1] == '#':
        return {}
    bits = line.split('\t')
    id = bits[0]
    chromosome = bits[1]
    position = bits[2]
    genotype = bits[3]
    return {
            "id": id,
            "genotype": genotype,
            "chromosome": chromosome,
            "position": position}


def print_mismatch(mrec, frec, crec):
    fmt = "MISMATCH! id: {:<12}  chr: {:>2} pos: {:>10} mg: {:2} fg: {:2} cg: {:2}"     # noqa
    print (fmt.format(mrec["id"],
                      mrec["chromosome"],
                      mrec["position"],
                      mrec["genotype"],
                      frec["genotype"],
                      crec["genotype"]))


def compare_genotypes(mrec, frec, crec):
    mg = mrec["genotype"]
    fg = frec["genotype"]
    cg = crec["genotype"]

    # Ignore missing data
    if mg == "--" or fg == "--" or cg == "--":
        return True
    if len(mg) < 2 or len(fg) < 2 or len(cg) < 2:
        return True

    # Check 'em
    if cg[0] in mg and cg[1] in fg:
        return True
    if cg[0] in fg and cg[1] in mg:
        return True

    # No match?
    return False


def main(mother, father, child):
    mismatches = 0
    with open(mother, "r") as mp:
        with open(father, "r") as fp:
            with open(child, "r") as cp:
                num = 0
                while True:
                    mrec = parse(mp)
                    frec = parse(fp)
                    crec = parse(cp)
                    if mrec is None or frec is None or crec is None:
                        if mrec is not None or frec is not None or crec is not None:    # noqa
                            print "END, but INCOMPLETE!"
                        else:
                            print "END!"
                        break
                    if len(mrec) == 0 or len(frec) == 0 or len(crec) == 0:
                        continue
                    num += 1
                    if mrec["id"] != frec["id"] or frec["id"] != crec["id"]:
                        print "DIFFER!"
                        break
                    if num > 1000000:
                        print "LIMIT!"
                        break

                    if not compare_genotypes(mrec, frec, crec):
                        mismatches += 1
                        if mismatches < 200:
                            print_mismatch(mrec, frec, crec)
    print "Total mismatches:", mismatches


if len(sys.argv) < 4:
    print "You must specify the files: mother father child"
    sys.exit(1)

main(sys.argv[1], sys.argv[2], sys.argv[3])
