#!/bin/bash

psql postgresql://applications:interlinked@localhost:5432/portfolio -a -f db-init.sql
