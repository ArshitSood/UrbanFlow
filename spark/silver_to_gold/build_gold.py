from __future__ import annotations

from pyspark.sql import DataFrame, functions as F


AIRPORT_LOCATION_IDS = [1, 132, 138]


def hourly_zone_demand(silver: DataFrame) -> DataFrame:
    return (
        silver.withColumn("pickup_hour", F.date_trunc("hour", "pickup_at"))
        .groupBy("trip_date", "pickup_hour", "service_type", "pickup_location_id")
        .agg(
            F.count("*").alias("trip_count"),
            F.sum("passenger_count").alias("passenger_count"),
            F.avg("trip_duration_minutes").alias("avg_duration_minutes"),
        )
    )


def route_performance(silver: DataFrame) -> DataFrame:
    return (
        silver.groupBy("trip_date", "service_type", "pickup_location_id", "dropoff_location_id")
        .agg(
            F.count("*").alias("trip_count"),
            F.avg("trip_duration_minutes").alias("avg_duration_minutes"),
            F.expr("percentile_approx(trip_duration_minutes, 0.5)").alias("median_duration_minutes"),
            F.avg("trip_distance_miles").alias("avg_distance_miles"),
            F.avg("total_amount").alias("avg_total_amount"),
        )
    )


def airport_metrics(silver: DataFrame) -> DataFrame:
    return (
        silver.where(
            F.col("pickup_location_id").isin(AIRPORT_LOCATION_IDS)
            | F.col("dropoff_location_id").isin(AIRPORT_LOCATION_IDS)
        )
        .withColumn(
            "airport_location_id",
            F.when(F.col("pickup_location_id").isin(AIRPORT_LOCATION_IDS), F.col("pickup_location_id"))
            .otherwise(F.col("dropoff_location_id")),
        )
        .groupBy("trip_date", "service_type", "airport_location_id")
        .agg(
            F.count("*").alias("trip_count"),
            F.avg("trip_duration_minutes").alias("avg_duration_minutes"),
            F.avg("total_amount").alias("avg_total_amount"),
        )
    )


def revenue_metrics(silver: DataFrame) -> DataFrame:
    return (
        silver.groupBy("trip_date", "service_type")
        .agg(
            F.count("*").alias("trip_count"),
            F.sum("fare_amount").alias("fare_amount"),
            F.sum("tip_amount").alias("tip_amount"),
            F.sum("tolls_amount").alias("tolls_amount"),
            F.sum("total_amount").alias("total_amount"),
        )
    )


def mobility_metrics(silver: DataFrame) -> DataFrame:
    return (
        silver.groupBy("trip_date", "service_type")
        .agg(
            F.count("*").alias("trip_count"),
            F.avg("trip_duration_minutes").alias("avg_duration_minutes"),
            F.expr("percentile_approx(trip_distance_miles, 0.5)").alias("median_distance_miles"),
            F.countDistinct("pickup_location_id").alias("active_pickup_zones"),
            F.countDistinct("dropoff_location_id").alias("active_dropoff_zones"),
        )
    )

