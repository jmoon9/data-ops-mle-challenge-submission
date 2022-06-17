resource "aws_ecr_repository" "ecr" {
    name                    = "${var.name_prefix}-${var.environment}-ecr"
    image_tag_mutability    = "MUTABLE"

    tags = var.tags
}

resource "aws_ecr_repository_policy" "ecr_policy" {
    repository = aws_ecr_repository.ecr.name

    policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "new policy",
            "Effect": "Allow",
            "Principal": {
                "AWS": [
                    "arn:aws:iam::683339921237:user/jenkins-bitcoin-predictor-user"
                ]
            },
            "Action": [
                "ecr:GetDownloadUrlForLayer",
                "ecr:BatchGetImage",
                "ecr:BatchCheckLayerAvailability",
                "ecr:PutImage",
                "ecr:InitiateLayerUpload",
                "ecr:UploadLayerPart",
                "ecr:CompleteLayerUpload",
                "ecr:DescribeRepositories",
                "ecr:GetRepositoryPolicy",
                "ecr:ListImages",
                "ecr:DeleteRepository",
                "ecr:BatchDeleteImage",
                "ecr:SetRepositoryPolicy",
                "ecr:DeleteRepositoryPolicy"
            ]
        }
    ]
}
EOF
}


