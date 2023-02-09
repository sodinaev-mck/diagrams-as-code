from diagrams import Cluster, Diagram
from diagrams.aws.compute import ECS, EKS, Lambda, EC2
from diagrams.aws.storage import S3
from diagrams.aws.devtools import Codecommit
from diagrams.aws.database import DB
from diagrams.aws.network import ALB
from diagrams.aws.general import General
from diagrams.programming.language import Bash
from diagrams.onprem.iac import Terraform
from diagrams.saas.identity import Okta
from diagrams.custom import Custom

with Diagram("Compliance Service", show=False, filename="compliance-service"):
    with Cluster("User env"):
        mcli = [Bash("Compliance CLI"), Terraform("IaC"), Okta("SSO/SAML")]



    with Cluster("Compliance Service"):
        alb = ALB("Compliance endpoint")
        with Cluster("Engine"):
            workers = [ECS("workflow A"),
                       ECS("workflow B"),
                       ECS("workflow C")]

        policies = Codecommit("Compliance rules")
        workers >> policies
        mcli >> alb >> workers

    with Cluster("Landing Zone"):
        with Cluster("Dev env"):
            pg_state_bucket = S3("state-bucket")
            pg_resource = General("Resource")

    checked = Custom("Compliant \n IaC", "./icons/checked.png")

    policies >> checked >> pg_resource