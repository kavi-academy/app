# Expenses Manager Application

This repository holds the source code for the **Expenses‑Manager** web/service.  It is language‑agnostic – you can implement it in Java, Python, Node‑JS, etc.  The repository should contain:

```
app/
├─ src/               # application source
│   └─ ...
├─ Dockerfile         # builds a container image for the app
├─ Jenkinsfile        # CI pipeline definition (will be used by the Jenkins server provisioned in infra)
└─ README.md
```

The `Dockerfile` must produce an image that can be pushed to the ECR repository created by the **infra** Terraform.  The `Jenkinsfile` will checkout this repo, run tests, build the Docker image, push to ECR, and finally trigger a Terraform apply for the target environment.
