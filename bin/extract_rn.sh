#!/bin/bash

if [[ -z $1 ]]; then
    echo "ERROR: Missing pdf file!"
    exit 1
fi

mkdir -p pdf

names=$(qpdf --json "$1" | grep title | sed -e 's/^[ \t]*//' | sort | uniq | awk -F: '{print $2}' | sed 's/"//g')
i=3
IFS=$'\n'
for name in ${names[@]}; do
    name=$(echo ${name:1} | tr ' ' '_')
    qpdf "$1" --pages . $i -- pdf/${name}.pdf
    i=$((i+1))
done

tar czvf pdf.tar.gz pdf
