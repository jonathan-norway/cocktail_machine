#!/bin/env bash

pkill -f mixmaster
git pull origin main
pip install -e .
