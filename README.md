# oshinko temaki

[![Build Status](https://travis-ci.org/elmiko/oshinko-temaki.svg?branch=master)](https://travis-ci.org/elmiko/oshinko-temaki)

hand rolled spark clusters for openshift

## overview

This is a console utility to make creating Spark clusters with the
[spark-operator](https://github.com/radanalyticsio/spark-operator) simpler.
When invoked it will print a cluster schema to standard output using the
requested options.

## get started

```
pip install oshinko_temaki
```

to create a cluster where the spark-operator is running

```
osht | oc apply -f -
```

for more details

```
osht -h
```
