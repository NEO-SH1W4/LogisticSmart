@echo off
echo Iniciando o aplicativo LogisticSmart...
streamlit run LogisticSmart_v1.py --server.enableXsrfProtection false --server.enableCORS false --server.address 0.0.0.0 --server.port 8501
echo.
echo Pressione qualquer tecla para fechar...
pause > nul
