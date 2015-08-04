#!/bin/basj

set -ev

pushd distrib/build
make predownload
make build
popd

