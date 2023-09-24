#!/bin/bash

# Start the first process
streamlit run ui/streamlit_app.py --server.port 8888 &
# Start the second process
gunicorn app:app &
# Wait for any process to exit
wait -n
# Exit with status of process that exited first
exit $?