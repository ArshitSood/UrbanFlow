from __future__ import annotations

from pyspark.sql import DataFrame, functions as F


SERVICE_TIMESTAMP_COLUMNS = {
    "yellow": ("tpep_pickup_datetime", "tpep_dropoff_datetime"),
    "green": ("lpep_pickup_datetime", "lpep_dropoff_datetime"),
    "fhvhv": ("pickup_datetime", "dropoff_datetime"),
}


def canonicalize_trips(bronze: DataFrame, service: str) -> DataFrame:
    pickup_col, dropoff_col = SERVICE_TIMESTAMP_COLUMNS[service]
    return (
        bronze.withColumn("service_type", F.lit(service))
        .withColumn("pickup_at", F.to_timestamp(F.col(pickup_col)))
        .withColumn("dropoff_at", F.to_timestamp(F.col(dropoff_col)))
        .withColumn("pickup_location_id", F.col("PULocationID").cast("int"))
        .withColumn("dropoff_location_id", F.col("DOLocationID").cast("int"))
        .withColumn("trip_distance_miles", F.col("trip_distance").cast("double"))
        .withColumn("passenger_count", F.col("passenger_count").cast("int"))
        .withColumn("fare_amount", F.col("fare_amount").cast("double"))
        .withColumn("tip_amount", F.col("tip_amount").cast("double"))
        .withColumn("tolls_amount", F.col("tolls_amount").cast("double"))
        .withColumn("total_amount", F.col("total_amount").cast("double"))
        .withColumn(
            "trip_duration_minutes",
            (F.unix_timestamp("dropoff_at") - F.unix_timestamp("pickup_at")) / F.lit(60.0),
        )
        .withColumn(
            "average_speed_mph",
            F.when(
                (F.col("trip_distance_miles") > 0) & (F.col("trip_duration_minutes") > 0),
                F.col("trip_distance_miles") / (F.col("trip_duration_minutes") / F.lit(60.0)),
            ),
        )
        .withColumn("trip_date", F.to_date("pickup_at"))
        .select(
            "service_type",
            "pickup_at",
            "dropoff_at",
            "trip_date",
            "pickup_location_id",
            "dropoff_location_id",
            "passenger_count",
            "trip_distance_miles",
            "trip_duration_minutes",
            "average_speed_mph",
            "fare_amount",
            "tip_amount",
            "tolls_amount",
            "total_amount",
            "_source_file",
            "_ingestion_id",
            "_ingested_at",
            "_schema_version",
        )
    )


def split_valid_invalid(canonical: DataFrame) -> tuple[DataFrame, DataFrame]:
    reason = (
        F.when(F.col("pickup_at").isNull(), F.lit("malformed_pickup_timestamp"))
        .when(F.col("dropoff_at").isNull(), F.lit("malformed_dropoff_timestamp"))
        .when(F.col("dropoff_at") <= F.col("pickup_at"), F.lit("non_positive_duration"))
        .when(F.col("pickup_location_id").isNull(), F.lit("missing_pickup_location"))
        .when(F.col("dropoff_location_id").isNull(), F.lit("missing_dropoff_location"))
        .when(F.col("trip_distance_miles") < 0, F.lit("negative_distance"))
        .when(F.col("total_amount") < 0, F.lit("negative_total_amount"))
    )
    evaluated = canonical.withColumn("rejection_code", reason)
    valid = evaluated.where(F.col("rejection_code").isNull()).drop("rejection_code")
    invalid = evaluated.where(F.col("rejection_code").isNotNull()).withColumn(
        "rejection_reason",
        F.concat(F.lit("Rejected by deterministic Silver contract: "), F.col("rejection_code")),
    )
    return valid, invalid

