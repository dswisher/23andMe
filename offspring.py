
import sys


def parse(fp):
    line = fp.readline().strip()
    if line == "":
        return None
    if line[:1] == '#':
        return {}
    bits = line.split('\t')
    id = bits[0]
    # chromosome = bits[1]
    # position = bits[2]
    genotype = bits[3]
    return {"id": id, "genotype": genotype}


def main(mother, father, child):
    with open(mother, "r") as mp:
        with open(father, "r") as fp:
            with open(child, "r") as cp:
                num = 0
                while True:
                    mrec = parse(mp)
                    frec = parse(fp)
                    crec = parse(cp)
                    if mrec is None or frec is None or crec is None:
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


if len(sys.argv) < 4:
    print "You must specify the files: mother father child"
    sys.exit(1)

main(sys.argv[1], sys.argv[2], sys.argv[3])
