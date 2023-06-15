FROM python:3

WORKDIR api

COPY requirements.txt /api

RUN pip install --no-cache-dir -r requirements.txt

COPY test_posts.py /api

COPY validation /api/validation

COPY __init__.py /api

CMD ["pytest", "-rA", "--tb=line"]