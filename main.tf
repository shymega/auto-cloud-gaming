data "aws_region" "current" {}
data "aws_caller_identity" "this" {}
data "aws_ecr_authorization_token" "ecr_token" {}

provider "docker" {
  registry_auth {
    address  = format("%v.dkr.ecr.%v.amazonaws.com", data.aws_caller_identity.this.account_id, data.aws_region.current.name)
    username = data.aws_ecr_authorization_token.ecr_token.user_name
    password = data.aws_ecr_authorization_token.ecr_token.password
  }
}

locals {
  prefix              = "cloud-gaming-rig"
  account_id          = data.aws_caller_identity.this.account_id
  ecr_repository_name = "${local.prefix}-lambda-telegram-bot"
  ecr_image_tag       = "latest"
}

module "lambda_function_container_image" {
  source = "terraform-aws-modules/lambda/aws"

  function_name = local.ecr_repository_name
  create_package = false

  image_uri     = module.docker_image.image_uri
  package_type  = "Image"
  architectures = ["x86_64"]
}

module "docker_image" {
  source = "terraform-aws-modules/lambda/aws//modules/docker-build"

  create_ecr_repo = true
  ecr_repo        = local.ecr_repository_name
  ecr_repo_lifecycle_policy = jsonencode({
    "rules" : [
      {
        "rulePriority" : 1,
        "description" : "Keep only the last 2 images",
        "selection" : {
          "tagStatus" : "any",
          "countType" : "imageCountMoreThan",
          "countNumber" : 2
        },
        "action" : {
          "type" : "expire"
        }
      }
    ]
  })

  image_tag   = "latest"
  source_path = "lambda/functions/telegram_bot"
  platform = "linux/amd64"
}
