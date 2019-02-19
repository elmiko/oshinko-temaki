import argparse
import uuid

from oshinko_temaki import templates

def generate_name():
    name = 'spark-{}'.format(uuid.uuid4().hex[-4:])
    return name


def main():
    """main entry point for the cli tool"""
    parser = argparse.ArgumentParser(description="create spark cluster configs")
    parser.add_argument("-n", "--name",
                        dest="name",
                        help="name of the spark cluster",
                        default=generate_name())
    parser.add_argument("-m", "--masters",
                        dest="masters",
                        help="number of master nodes",
                        type=int,
                        default=1)
    parser.add_argument("-w", "--workers",
                        dest="workers",
                        help="number of worker nodes",
                        type=int,
                        default=1)
    parser.add_argument("-i", "--image",
                        dest="image",
                        help="Spark cluster image to use")
    parser.add_argument("--crd",
                        dest="crd",
                        help="set if the output should be a CRD",
                        action="store_true")
    args = parser.parse_args()
    if args.crd is True:
        cluster = templates.CRDTemplate(args.name,
                                        args.masters,
                                        args.workers,
                                        args.image)
    else:
        cluster = templates.CMTemplate(args.name,
                                       args.masters,
                                       args.workers,
                                       args.image)
    print(cluster.dumps())


if __name__ == "__main__":
    main()
