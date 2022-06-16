variable "aws_region" {}
variable "aws_deployment_account_number" {}
variable "aws_access_key" {}
variable "aws_secret_access_key"{}
variable "environment" {}

variable "tags" {
    type = map(string)
    description = "tags to apply to the resources"
    default     = {
        createdBy   = "Terraform"
        owner       = "jmoon"
        project     = "bitcoin-predictor"
    }
}

locals {
    environment     = "${var.environment}"
}

locals {
    tags = merge(var.tags, { "environment" = "${local.environment}"})
    name_prefix = "${var.tags.project}-${local.environment}"
}

variable "sagemaker_ecr" {
    type    = string
    default = "683339921237.dkr.ecr.us-east-2.amazonaws.com"
}

variable "sagemaker_ecr_image_name" {
    type    = string
    default = "bitcoin-predictor"
}

variable "sagemaker_ecr_image_tag" {
    type    = string
    default = "latest"
}

variable "sagemaker_model_artifact_bucket" {
    type    = string
    default = "bitcoin-predictor-data-${local.environment}"
}

variable "sagemaker_model_artifact_bucket_region" {
    type    = string
    default = "us-east-2"
}

variable "sagemaker_model_artifact_file_name" {
    type    = string
    default = "bitcoin.csv"
}