# 2025-01-15
# The /pig_ops/data inside the container is a mounted directory of the the 
# container host.
# When a docker image a volume option like this 
#
# docker run -it -v ~/projects/pig_ops/pig_ops/data:/pig_ops/data  -p 80:5000 b26fbcd88e4e
#
# The mounted directory has this ownership
#
# drwxrwxr-x 3 1000 1000 4096 Jan 15 07:58 data
# drwxr-xr-x 2 root root 4096 Jan 15 07:46 __pycache__
#
# Need to change the ownership and group to root before any application run

chown root:root /pig_ops/data
