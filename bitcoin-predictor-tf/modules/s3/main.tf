resource "aws_s3_bucket" "b" {
    bucket = "${var.name_prefix}-data-${var.environment}"
    acl    = "private"

    tags = var.tags
}

# resource "aws_s3_bucket_policy" "b" {
#     bucket = aws_s3_bucket.b.id

#     # Terraform's "jsonencode" function converts a
#     # Terraform expression's result to valid JSON syntax.
#     policy = jsonencode({
#         Version = "2012-10-17"
#         Id      = "MYBUCKETPOLICY"
#         Statement = [
#             {
#                 Sid       = "Allow"
#                 Effect    = "Deny"
#                 Principal = "*"
#                 Action    = "s3:*"
#                 Resource = [
#                     aws_s3_bucket.b.arn,
#                     "${aws_s3_bucket.b.arn}/*",
#                 ]
#             },
#         ]
#     })
# }