# ECS Infra - main.tf

provider "aws" {
  region = var.aws_region
}

# ECR Repository
resource "aws_ecr_repository" "budget_app_repo" {
  name = "budget-app-django"
}

# IAM Role for ECS Task Execution
resource "aws_iam_role" "ecs_task_execution_role" {
  name = "ecsTaskExecutionRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action    = "sts:AssumeRole",
      Effect    = "Allow",
      Principal = {
        Service = "ecs-tasks.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution_policy" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# ECS Cluster
resource "aws_ecs_cluster" "budget_app_cluster" {
  name = "BudgetAppCluster"
}

# ECS Task Definition
resource "aws_ecs_task_definition" "budget_app_task" {
  family                   = "budget-app-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn

  container_definitions = jsonencode([
    {
      name      = "budget-app-django",
      image     = "650251691774.dkr.ecr.ap-southeast-1.amazonaws.com/budget-app-django:latest",
      essential = true,
      portMappings = [
        {
          containerPort = 8000,
          hostPort      = 8000
        }
      ]
    }
  ])
}

# ECS Service
resource "aws_ecs_service" "budget_app_service" {
  name            = "NewBudgetAppFargate"
  cluster         = aws_ecs_cluster.budget_app_cluster.id
  task_definition = aws_ecs_task_definition.budget_app_task.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets         = var.subnet_ids
    security_groups = [var.security_group_id]
    assign_public_ip = true
  }

  lifecycle {
    ignore_changes = [task_definition]
  }
}

# Variables
variable "aws_region" {
  default = "ap-southeast-1"
}

variable "subnet_ids" {
  type = list(string)
}

variable "security_group_id" {
  type = string
}

output "ecr_repo_url" {
  value = aws_ecr_repository.budget_app_repo.repository_url
}

output "ecs_cluster_name" {
  value = aws_ecs_cluster.budget_app_cluster.name
}

output "ecs_service_name" {
  value = aws_ecs_service.budget_app_service.name
}
