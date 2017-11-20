import scala.io.Source
import java.util.zip.ZipInputStream
import org.apache.spark.input.PortableDataStream
import org.apache.hadoop.io.compress.GzipCodec
import org.apache.spark.sql.types.MetadataBuilder

val inputFile = "s3://download.open.fda.gov/food/enforcement/*.json.zip";
val outputDir = "s3://<Your S3 Bucket Name>/food/enforcement/";

// Process zip file to extract the json as text file and save it in the output directory 
val rdd = sc.binaryFiles(inputFile).flatMap((file: (String, PortableDataStream)) => {
    val zipStream = new ZipInputStream(file._2.open)
    val entry = zipStream.getNextEntry
    val iter = Source.fromInputStream(zipStream).getLines
    iter
}).saveAsTextFile(outputDir, classOf[GzipCodec])


val df =  spark.read.json(sc.wholeTextFiles("s3://<Your S3 Bucket Name>/food/enforcement/").values)

var results = df.withColumn("results", explode($"results"))

results = results.select("results.address_1",
                            "results.address_2", 
                            "results.center_classification_date",
                            "results.city",
                            "results.classification",
                            "results.code_info",
                            "results.country",
                            "results.distribution_pattern",
                            "results.event_id",
                            "results.initial_firm_notification",
                            "results.more_code_info",
                            "results.postal_code",
                            "results.product_description",
                            "results.product_quantity",
                            "results.product_type",
                            "results.reason_for_recall",
                            "results.recall_initiation_date",
                            "results.recall_number",
                            "results.recalling_firm",
                            "results.report_date",
                            "results.state",
                            "results.status",
                            "results.termination_date",
                            "results.voluntary_mandated")

//Extend the varchar length for strings larger than 250 characters
val columnLengthMap = Map("code_info" -> 32600, "distribution_pattern" -> 1294, "more_code_info" -> 9161,"product_description"-> 4001,"reason_for_recall" -> 1138)

// Apply each column metadata customization
columnLengthMap.foreach { case (colName, length) =>
  val metadata = new MetadataBuilder().putLong("maxlength", length).build()
  results = results.withColumn(colName, results(colName).as(colName, metadata))
}

results.write
  .format("com.databricks.spark.redshift")
  .option("url", "jdbc:redshift://<Your Redshift Host>:5439/dev?user=<Your Redshift Username>&password=<Your Redshift Password>")
  .option("dbtable", "food_enforcement")
  .option("tempdir", "s3n:// <Your S3 Bucket Name>/tmp/")
  .option("aws_iam_role", "<Your Redshift Role Arn>")
  .mode("overwrite")
  .save()