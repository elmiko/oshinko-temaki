import argparse

from oshinko_temaki import configs
from oshinko_temaki import templates


def main():
    """main entry point for the cli tool"""
    parser = argparse.ArgumentParser(description="create spark cluster configs")
    parser.add_argument("-n", "--name",
                        dest="name",
                        help="name of the spark cluster")
    parser.add_argument("-m", "--masters",
                        dest="masters",
                        help="number of master nodes",
                        type=int)
    parser.add_argument("-w", "--workers",
                        dest="workers",
                        help="number of worker nodes",
                        type=int)
    parser.add_argument("-i", "--image",
                        dest="image",
                        help="Spark cluster image to use")
    parser.add_argument("--crd",
                        dest="crd",
                        help="set if the output should be a CRD",
                        action="store_true")
    parser.add_argument("-t", "--metrics",
                        dest="metrics",
                        help="enable metrics deployment",
                        action="store_true")
    parser.add_argument("-u", "--ui",
                        dest="webui",
                        help="enable Spark master web ui route",
                        action="store_true")
    parser.add_argument("-c", "--configmap",
                        dest="configmap",
                        help="a configmap name to use for spark configuration")
    args = parser.parse_args()
    conf = configs.ClusterConfig(args)
    if args.crd is True:
        cluster = templates.CRDTemplate(conf)
    else:
        cluster = templates.CMTemplate(conf)

    print(cluster.dumps())


if __name__ == "__main__":
    main()
