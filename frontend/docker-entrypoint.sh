#!/bin/sh

echo "[INFO] - entrypoint - downloading"
npm install 
npm install socket.io-client


exec npm run dev -- --host --port 8080