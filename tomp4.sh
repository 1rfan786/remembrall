#!/usr/bin/env sh

ffmpeg -i "${1}" -acodec libfaac -b:a 128k -vcodec mpeg4 -b:v 1200k -flags +aic+mv4 "${2}"
