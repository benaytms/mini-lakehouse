variable "location" {
  description = "Project Location"
  default     = "sa-east-1"
}


variable "s3_bucket_name" {
  description = "My S3 Storage Bucket"
}


variable "s3_storage_class" {
  description = "S3 Bucket Storage Class"
  default     = "STANDARD_IA"
}

variable "localstack_endpoint" {
  description = "LocalStack endpoint URL"
  default     = "http://localhost:4566"
}