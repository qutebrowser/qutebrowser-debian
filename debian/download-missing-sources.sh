#!/bin/sh

D=$(dirname $0)
V=$(head -1 $D/changelog | awk -F'[-()]' '{print $2}')

cd $D/missing-sources/

for f in settings configuring; do
    wget -O ${f}.asciidoc \
         https://github.com/qutebrowser/qutebrowser/raw/v${V}/doc/help/${f}.asciidoc
done;
