#!/bin/bash
uvicorn trend_catcher.backend.main:app --host 0.0.0.0 --port 10000
