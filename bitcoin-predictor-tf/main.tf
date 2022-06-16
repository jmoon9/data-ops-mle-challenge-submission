provider "aws" {
    region = var.aws_region
    version = "~> 4.9.0"
    access_key = var.aws_access_key
    secret_key = var.aws_secret_access_key
}

terraform {
    backend "s3" {
        bucket          = "bitcoin-predictor-tf-backend"
        region          = "us-east-2"
        key             = "bitcoin-predictor-inference/bitcoin-predictor-inference-state.tfstate"
        encrypt         = true 
        role_arn        = //TODO: create arn assume role
    }
}

module "sagemaker-setup" {
    source = "./modules/sagemaker-inference"

    tags                = local.tags
    name_prefix         = local.name_prefix
    environment         = local.environment

    host_instance_count = 1
    host_instance_type  = "ml.t2.medium"

    model_artifact_source_bucket        = var.sagemaker_model_artifact_bucket
    model_artifact_source_bucket_region = var.sagemaker_model_artifact_bucket_region
    model_artifact_file_name            = var.sagemaker_model_artifact_file_name

    sagemaker_ecr               = var.sagemaker_ecr
    sagemaker_ecr_image_name    = var.sagemaker_ecr_image_name
    sagemaker_ecr_image_tag     = var.sagemaker_ecr_image_tag
}

# TODO: modules for ECR, IAM and s3