@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ============================================================
echo   Atualizando estatisticas NBA - temporada 2026-27
echo   Fonte: stats.nba.com (IP local, sem proxy)
echo   Destino: Supabase (credenciais do arquivo .env)
echo ============================================================
echo.

python supabase_quick_start.py

echo.
echo ============================================================
echo   Coleta finalizada. Pressione qualquer tecla para fechar.
echo ============================================================
pause >nul
