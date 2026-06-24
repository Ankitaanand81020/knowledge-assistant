# demo.ps1 â€” Quick demo of the AI Knowledge Assistant API
# Run this with: .\demo.ps1

$TOKEN   = "secret-knowledge-token-2024"
$HEADERS = @{
    "Authorization" = "Bearer $TOKEN"
    "Content-Type"  = "application/json"
}
$BASE = "http://localhost:8000"

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  AI Knowledge Assistant â€” Demo" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# Health check
Write-Host ""
Write-Host "1. Health Check" -ForegroundColor Yellow
$health = Invoke-RestMethod -Uri "$BASE/" -Method GET
Write-Host "   Status  : $($health.status)"
Write-Host "   Model   : $($health.model)"
Write-Host "   Chunks  : $($health.chunks_indexed)"
Write-Host "   Auth    : $($health.auth)"

# Ask questions
$questions = @(
    "What is the annual leave policy?",
    "When is payday?",
    "How do I reset my password?",
    "What branching strategy do we use?"
)

foreach ($q in $questions) {
    Write-Host ""
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host "Q: $q" -ForegroundColor Yellow
    Write-Host "==========================================" -ForegroundColor Cyan

    $body   = "{`"question`": `"$q`", `"top_k`": 3}"
    $result = Invoke-RestMethod -Uri "$BASE/ask" -Method POST -Headers $HEADERS -Body $body

    Write-Host "A: $($result.answer)" -ForegroundColor White
    Write-Host ""
    Write-Host "   Sources:" -ForegroundColor Gray
    foreach ($c in $result.citations) {
        Write-Host "     - $($c.title) ($($c.similarity)% match)" -ForegroundColor Gray
    }
    Write-Host "   Latency: $($result.latency_ms)ms" -ForegroundColor Gray
}

# Stats
Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  Usage Stats" -ForegroundColor Yellow
Write-Host "==========================================" -ForegroundColor Cyan
$stats = Invoke-RestMethod -Uri "$BASE/stats" -Method GET
Write-Host "   Total queries   : $($stats.total_queries)"
Write-Host "   Avg latency     : $($stats.average_latency_ms)ms"
Write-Host "   PII detections  : $($stats.pii_detections)"
Write-Host ""
