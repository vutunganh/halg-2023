#!/bin/bash
set -e

if [ "$HOSTNAME" != nikam -o "$USER" != halg ] ; then
    echo "Run me as halg@nikam, please"
    exit 1
fi

DEST=~/registration
. $DEST/venv/bin/activate
pip install .

if [ -e $DEST/var/uwsgi.fifo ] ; then
    echo "Reloading uwsgi"
    echo r >$DEST/var/uwsgi.fifo || true
else
    echo "Restarting uwsgi"
    systemctl --user restart halg_reg
fi

