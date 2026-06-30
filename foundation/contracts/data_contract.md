# Data Contract

Raw data is immutable. Processed data is code-generated.

Every reportable dataset should record:

- dataset ID;
- version;
- source IDs;
- storage path;
- row and column counts;
- hash when available;
- sensitivity status;
- quality status;
- transformation code or config;
- known limitations.

DuckDB and Parquet are the canonical structured research data layer when a
project needs one. CSV remains acceptable for small, inspectable examples.
