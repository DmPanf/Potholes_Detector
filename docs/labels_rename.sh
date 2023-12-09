#!/bin/bash
# labels_rename.sh

for i in frame_*.txt; do
    mv "$i" "${i//frame_/v01p2_}"
done

