Run docker image

1.) Search for the docker image to run
ubuntu@ip-172-31-23-184:~$ docker images
REPOSITORY   TAG       IMAGE ID       CREATED          SIZE
pig_ops      latest    b26fbcd88e4e   14 minutes ago   1.37GB
python       3.12      acda8b87a53f   5 weeks ago      1.02GB
ubuntu       latest    b1d9df8ab815   7 weeks ago      78.1MB

2.) Map port 80 of the AWS EC2 host to docker proxy
ubuntu@ip-172-31-23-184:~/projects/pig_ops/pig_ops$ docker run -it -p 80:5000 b26fbcd88e4e

ubuntu@ip-172-31-23-184:~/projects/pig_ops/pig_ops$ docker run -it -v ~/projects/pig_ops/pig_ops/data:/pig_ops/data  -p 80:5000 b26fbcd88e4e