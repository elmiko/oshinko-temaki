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
    parser.add_argument("-e", "--env",
                        dest="envs",
                        action="append",
                        help="add environment variable to set in cluster, "
                             "example --env KEY=VALUE")
    parser.add_argument("-s", "--sparkconfig",
                        dest="sparkconfigs",
                        action="append",
                        help="add a spark configuration variable to the "
                             "cluster, example --sparkconfig KEY=VALUE")
    parser.add_argument("-d", "--download",
                        dest="downloads",
                        action="append",
                        help="add a URL and directory to download data, "
                             "example --download URL::DIR")
    parser.add_argument("-o", "--output",
                        dest="output",
                        choices=["cr", "cm"],
                        default="cr",
                        help="specify the output type, custom resource (cr) "
                             "or ConfigMap (cm). default is cr")

    args = parser.parse_args()
    conf = configs.ClusterConfig(args)
    if args.output == "cr":
        cluster = templates.CRDTemplate(conf)
    else:
        cluster = templates.CMTemplate(conf)

    print(cluster.dumps())


if __name__ == "__main__":
    main()
