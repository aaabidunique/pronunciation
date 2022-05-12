# pronunciation
API for pronunciation using python and Google TTS

docker build -t pronunciation .

docker run --rm --name pronunciation -e PORT=8080 -p 8080:8080 pronunciation
