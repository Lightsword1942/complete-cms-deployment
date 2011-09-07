#!/bin/bash
rsync -av -e "ssh -l vagrant" 10.0.0.20:/pg_archive /pg_archive
