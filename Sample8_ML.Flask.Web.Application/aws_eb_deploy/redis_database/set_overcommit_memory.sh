#!/bin/bash

# Set overcommit memory for Redis
sysctl -w vm.overcommit_memory=1

# Execute the provided CMD arguments
exec "$@"
