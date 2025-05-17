#!/bin/sh
# https://hub.docker.com/r/microsoft/mssql-tools/

docker pull mcr.microsoft.com/mssql-tools

docker run -it --rm mcr.microsoft.com/mssql-tools
