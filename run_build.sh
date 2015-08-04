#!/bin/bash

set -ev

pushd distrib/build
make predownload
make build
popd

