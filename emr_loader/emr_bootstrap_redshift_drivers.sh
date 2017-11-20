#!/bin/bash

sudo wget http://central.maven.org/maven2/com/databricks/spark-redshift_2.11/3.0.0-preview1/spark-redshift_2.11-3.0.0-preview1.jar /usr/lib/spark/jars/spark-redshift_2.11-3.0.0-preview1.jar
sudo wget https://s3.amazonaws.com/redshift-downloads/drivers/RedshiftJDBC42-1.2.10.1009.jar /usr/lib/spark/jars/RedshiftJDBC42-1.2.10.1009.jar
sudo wget http://central.maven.org/maven2/com/databricks/spark-avro_2.11/4.0.0/spark-avro_2.11-4.0.0.jar /usr/lib/spark/jars/spark-avro_2.11-4.0.0.jar