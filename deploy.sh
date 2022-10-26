#!/bin/sh

rsync -r --chmod=u=rwX,go=rX www/ halg@kam.mff.cuni.cz:~/www
