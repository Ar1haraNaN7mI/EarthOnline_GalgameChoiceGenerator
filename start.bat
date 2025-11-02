@echo off
echo Starting AR Galgame Assistant...
echo.
echo Installing dependencies...
cd backend
pip install -r requirements.txt
echo.
echo Starting server...
python app.py
pause

