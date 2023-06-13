#!/bin/env bash

alembic upgread head

gunicorn run:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
