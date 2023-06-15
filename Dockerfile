FROM python:3

WORKDIR pythonProject12

COPY requirements.txt /pythonProject12

RUN pip install --no-cache-dir -r requirements.txt

COPY test_posts.py /pythonProject12

COPY validation /pythonProject12/validation

COPY __init__.py /pythonProject12

CMD ["pytest"]