#!/bin/bash
# run.sh - Simple script to start the Knowledge Assistant

set -e

echo "🚀 Starting Knowledge Assistant..."
echo ""

# Check if ollama is running
echo "Checking Ollama connection..."
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "❌ Ollama is not running!"
    echo "   Start it with: ollama serve"
    exit 1
fi
echo "✅ Ollama is running"

echo ""
echo "Starting services in background..."
echo ""

# Start backend
cd backend
echo "📌 Backend starting on http://localhost:8000"
python -m uvicorn main:app --reload --port 8000 > /tmp/backend.log 2>&1 &
BACKEND_PID=$!
echo "   PID: $BACKEND_PID"

cd ..

# Start frontend
cd frontend
echo "📌 Frontend starting on http://localhost:3000"
npm run dev > /tmp/frontend.log 2>&1 &
FRONTEND_PID=$!
echo "   PID: $FRONTEND_PID"

cd ..

echo ""
echo "✅ Services started!"
echo ""
echo "URLs:"
echo "  Frontend:  http://localhost:3000"
echo "  Backend:   http://localhost:8000"
echo "  API docs:  http://localhost:8000/docs"
echo ""
echo "Logs:"
echo "  Backend:  tail -f /tmp/backend.log"
echo "  Frontend: tail -f /tmp/frontend.log"
echo ""
echo "To stop: pkill -f uvicorn && pkill -f 'next dev'"
echo ""
echo "Press Ctrl+C to exit this script (services will keep running)"

trap "echo 'Services still running in background.'" EXIT

# Wait for keyboard interrupt
while true; do
    sleep 1
done
