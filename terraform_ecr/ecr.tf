provider "aws" {
  region = "eu-west-2"
}

resource "aws_ecr_repository" "event_finder" {
  name = "event-finder"
}

resource "aws_ecr_repository" "emailer" {
  name = "emailer"
}

output "ecr_repos" {
  value = {
    event_finder = aws_ecr_repository.event_finder.repository_url
    emailer = aws_ecr_repository.emailer.repository_url
  }
}