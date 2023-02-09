from diagrams import Cluster, Diagram
from diagrams.aws.compute import ECR, Fargate, ElasticContainerServiceService as Svc, ElasticContainerServiceContainer as Task
from diagrams.aws.storage import S3
from diagrams.aws.network import NLB

with Diagram("Using NLB with ECS", show=False, filename="dist/nlb-ecs"):

    with Cluster("Proving Ground"):
        nlb = NLB("NLB tcp/5000")
        s3 = S3("Access Logs")
        nlb >> s3

        with Cluster("ECS"):
            service = Svc("Service")
            fargate = Fargate("Fargate")
            fargate >> service
            with Cluster("AutoScaling cluster"):
                tasks = [Task("tcp/5000") for i in range(3)]
            ecr = ECR("ECR Repo")
            service >> tasks >> ecr
        nlb >> service
