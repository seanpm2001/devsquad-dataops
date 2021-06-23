#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyspark.sql import SparkSession
try:
    import dataopslib.spark.data_quality as quality
    import dataopslib.schemas as schemas
except ImportError:
    import os
    import sys
    cur_dir = os.path.dirname(__file__)
    # Add the parent directory in the search for modules when importing
    sys.path.append(os.path.abspath(os.path.join(cur_dir, os.pardir)))
    import dataopslib.spark.data_quality as quality
    import dataopslib.schemas as schemas


spark = SparkSession.builder\
    .master("local")\
    .appName("sample_has_valid_dates.py")\
    .getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

schema = schemas.get_schema("sample_schema")
df = spark.read.csv("./data/sample_data.csv", header=True, schema=schema)

cols = ['END_DATE', 'START_DATE']
has_invalid_dates = quality.has_invalid_dates(df, cols, 'MM/dd/yyyy HH:mm:ss')
if has_invalid_dates:
    print("The dataframe has invalid dates in the columns", cols)
else:
    print("The dataframe doesn't have invalid dates in the columns", cols)
