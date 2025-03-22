@echo off
title 🚀 Iniciando LogisticSmart - Web App
echo.
echo Abrindo o aplicativo Logístico Inteligente...
streamlit run LogisticSmart_v1.py --server.enableXsrfProtection false --server.enableCORS false --server.address 0.0.0.0 --server.port 8501
pause
