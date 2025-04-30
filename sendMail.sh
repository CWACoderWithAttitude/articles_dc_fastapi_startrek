#!/bin/sh
# https://stackoverflow.com/questions/14722556/using-curl-to-send-email
#curl --ssl-reqd \
curl  \
  --url 'smtp://mailcatcher.local:1025' \
  --user 'username@gmail.com:password' \
  --mail-from 'username@gmail.com' \
  --mail-rcpt 'john@example.com' \
  --upload-file mail.txt