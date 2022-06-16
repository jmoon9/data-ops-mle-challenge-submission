output "URL" {
    value = "https://runtime.sagemaker.${data.aws_region.current.name}.amazonaws.com/endpoints/${aws_sagemaker_endpoint.endpoint.name}/invocations"
}