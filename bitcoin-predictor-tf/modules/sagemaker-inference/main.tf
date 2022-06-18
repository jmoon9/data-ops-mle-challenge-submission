data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

data "aws_s3_bucket_object" "object_source_1" {
    bucket  = var.model_artifact_source_bucket
    key     = var.model_artifact_file_name
}

data "aws_ecr_image" "sagemaker_ecr_image" {
    repository_name = var.sagemaker_ecr_image_name
    image_tag       = var.sagemaker_ecr_image_tag
}      

resource "aws_iam_role" "sagemaker_role" {
    name                = "${var.name_prefix}-sagemaker"
    path                = "/"
    assume_role_policy  = data.aws_iam_policy_document.assume_role.json
}

data "aws_iam_policy_document" "assume_role" {
    statement {
        actions = ["sts:AssumeRole"]

        principals {
            type        = "Service"
            identifiers = ["sagemaker.amazonaws.com"]
        }
    }
}

resource "aws_iam_policy" "sagemaker_policy" {
    name        = "${var.name_prefix}-sagemaker-policy"
    description = "Sagemaker model creation permissions"
    policy      = data.aws_iam_policy_document.sagemaker_policy.json
}

data "aws_iam_policy_document" "sagemaker_policy" {
    statement {
        effect  = "Allow"
        actions = [
            "sagemaker:*"
        ]
        resources = [
            "*"
        ]
    }
    statement {
        effect  = "Allow"
        actions = [
            "cloudwatch:PutMetricData",
            "logs:CreateLogStream",
            "logs:PutLogEvents",
            "logs:CreateLogGroups",
            "logs:DescribeLogStreams",
            "ecr:GetAuthorizationToken",
            "ecr:BatchCheckLayerAvailability",
            "ecr:GetDownloadUrlForLayer",
            "ecr:BatchGetImage"
        ]
        resources = [
            "*"
        ]
    }
    statement {
        effect  = "Allow"
        actions = [
            "s3:GetObject"
        ]
        resources = [
            "arn:aws:s3:::${var.model_artifact_source_bucket}",
            "arn:aws:s3:::${var.model_artifact_source_bucket}/*"
        ]
    }
}

resource "aws_iam_role_policy_attachment" "sagemaker_role_policy_attachment" {
    role = aws_iam_role.sagemaker_role.name
    policy_arn = aws_iam_policy.sagemaker_policy.arn
}

resource "aws_sagemaker_model" "model" {
    name = "${var.name_prefix}-model"
    execution_role_arn = aws_iam_role.sagemaker_role.arn

    primary_container {
        image = "${var.sagemaker_ecr}/${var.sagemaker_ecr_image_name}:${var.sagemaker_ecr_image_tag}"
        # model_data_url = "https://${var.model_artifact_source_bucket}.s3.${var.model_artifact_source_bucket_region}.amazonaws.com/${var.model_artifact_file_name}"
    }
    
    tags = var.tags
}

resource "aws_sagemaker_endpoint" "endpoint" {
    name                    = "${var.name_prefix}-endpoint"
    endpoint_config_name    = aws_sagemaker_endpoint_configuration.endpoint.name

    tags = var.tags
}

resource "aws_sagemaker_endpoint_configuration" "endpoint" {
    name    = "${var.name_prefix}-endpoint-config"
    
    production_variants {
        model_name        = aws_sagemaker_model.model.name
        initial_instance_count          = var.host_instance_count
        instance_type                   = var.host_instance_type
        variant_name                    = "${var.environment}-variant"
    }

    lifecycle {
        create_before_destroy = true
    }

    tags = var.tags
}