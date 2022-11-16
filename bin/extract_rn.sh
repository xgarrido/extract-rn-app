#!/bin/bash

if [[ -z $1 ]]; then
    echo "ERROR: Missing pdf file!"
    exit 1
fi

names=$(qpdf --json "$1" | grep title | sed -e 's/^[ \t]*//' | sort | uniq | awk -F: '{print $2}' | sed 's/"//g')
i=3
IFS=$'\n'
for name in ${names[@]}; do
    name=$(echo ${name:1} | tr ' ' '_')
    echo "**"$i $name
    pdfjam "$1" $i -o ${name}.pdf
    i=$((i+1))
done
