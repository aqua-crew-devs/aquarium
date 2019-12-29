#!/bin/sh

waitress-serve --port=5000 --call 'src:create_app'