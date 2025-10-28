#!/bin/bash

set -e
set -x

FILE="PHILOSOPHIE_DES_ABENDLANDES_VON_BERTRAND_RUSSEL_djvu.txt"
SHA="put_expected_sha256_here"

if [[ -f "$FILE" ]]; then
    ACTUAL_SHA=$(sha256sum "$FILE" | awk '{print $1}')
    if [[ "$ACTUAL_SHA" != "4d5c4df4acf91d91256267d247acfa1a6bf2c78e6df9cbe6377852f21a77271b" ]]; then
        echo "SHA256 mismatch! Not the file I expected"
    fi
else
    echo "File does not exist: $FILE"
    exit 1
fi


./clean.py
./split_chapters.py