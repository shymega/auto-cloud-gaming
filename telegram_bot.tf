data aws_caller_identity current {}

locals {
  prefix = "cloud-gaming-rig"
  account_id          = data.aws_caller_identity.current.account_id
  ecr_repository_name = "${local.prefix}-lambda-telegram-bot"
  ecr_image_tag = "latest"
}

resource aws_ecr_repository repo {
 name = local.ecr_repository_name
}
 
resource null_resource ecr_image {
provisioner "local-exec" {
command = <<EOF
           aws ecr get-login-password --region ${var.region} | docker login --username AWS --password-stdin ${local.account_id}.dkr.ecr.${var.region}.amazonaws.com
           cd ${path.module}/lambda/functions/telegram_bot
           docker build -t ${aws_ecr_repository.repo.repository_url}:${local.ecr_image_tag} .
           docker push ${aws_ecr_repository.repo.repository_url}:${local.ecr_image_tag}
       EOF
 }
}

data aws_ecr_image lambda_image {
 depends_on = [
   null_resource.ecr_image
 ]
 repository_name = local.ecr_repository_name
 image_tag       = local.ecr_image_tag
}
