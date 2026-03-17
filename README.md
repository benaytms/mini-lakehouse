# "Mini" Lakehouse Implementation

This project uses a series of data engineering tools to produce
a similar structure to a Lakehouse (Data Lake + Data Warehouse).

The purpose of a Lakehouse is to have both the long-term "cold" data,
records that are not intended to be accessed with frequency and serve more
to keep history like from Data Lakes, and short-term "fresh" data, which are records 
intended for quick and efficient access like from Data Warehouses.

---

## Architecture

The pipeline follows the **Medallion Architecture**, structured in three layers:

- **Bronze** — raw data as received from the source (JSON), stored in S3 with no transformations. Permanent record of every fetch.
- **Silver** — cleaned, typed, and flattened data written to S3 as Parquet. Optimized for analytical processing.
- **Gold** — aggregated data loaded into PostgreSQL tables, ready for querying and consumption.

### Data Workflow

```
API → S3/bronze/ (JSON) → S3/silver/ (Parquet) → PostgreSQL (Gold)
```

---

## Softwares Used

| Tool | Role |
|---|---|
| [Docker + Compose](https://docs.docker.com/engine/) | Container orchestration |
| [Terraform](https://developer.hashicorp.com/terraform/docs) | Infrastructure provisioning |
| [LocalStack](https://docs.localstack.cloud) | Local AWS S3 emulation |
| [PostgreSQL](https://www.postgresql.org/docs/) | Gold serving layer |
| [Python + pandas](https://pandas.pydata.org/) | Data transformation |
| [uv](https://docs.astral.sh/uv/) | Python package management |

---

## Prerequisites

- [Docker + Compose](https://docs.docker.com/compose/install/)
- [Terraform](https://developer.hashicorp.com/terraform/install)
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

---

## Setup

In case you want to test it, it's fairly straight forward.

1. Clone the repository
   ```bash
    git clone https://github.com/benaytms/mini-lakehouse.git
    cd mini-lakehouse
   ```
2. Create .env from example
    ```bash
    cp .env.example .env
    # open .env and fill in the variables
    ```
3. Configure Terraform variables
    ```bash
    cp terraform/terraform.tfvars.example terraform/terraform.tfvars
    # open terraform.tfvars and set your bucket name
    # must match BUCKET_NAME in .env
    ```
4. Run the pipeline
    ```bash
    make up     # starts containers and S3 bucket
    make run    # runs the full pipeline (Bronze->Silver->Gold)
    ```
5. Explore the data
   ```bash
   make psql
   ```
   Once inside, try:
    ```sql
    SELECT * FROM countries LIMIT 10;
    SELECT * FROM covid_cases LIMIT 10;
    ```
    Exit
   ```
   \q
   ```
6. Teardown
   ```bash
   make down    # clear bucket files, stops all containers
   docker container prune     # Removes all stopped containers 
                              # CAREFUL in case you have other stopped containers!)
   ```

---
## License

MIT



    