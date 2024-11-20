#!/bin/bash -xc
pip3 install -U pytest --no-warn-script
touch /tmp/empty1
touch /tmp/empty2
echo "cool1" > /tmp/cool1
echo "cool2" > /tmp/cool2
zip $HOME/$NAME/stub.zip /tmp/empty1 /tmp/empty2 /tmp/cool1 /tmp/cool2
rm -rf /tmp/empty1 /tmp/empty2 /tmp/cool1 /tmp/cool2