heroku ps:scale web=0
heroku ps:scale worker=1
worker: uvicorn app.main:app --host=0.0.0.0 --port=${PORT:-5000}