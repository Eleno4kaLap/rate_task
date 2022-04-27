# rate_task

**Task**

Write an API using Django that fetches the price of BTC/USD from the alphavantage API every hour, 
and stores it on postgres. This API must be secured which means that you will need an API key to use it. 
There should be two endpoints: GET /api/v1/quotes - returns exchange rate and 
POST /api/v1/quotes which triggers force requesting the prices from alphavantage.
The API & DB should be containerized using Docker as well. 

- The project should be committed to GitHub.
- The technologies to be used: Celery, Redis or RabbitMQ, Docker and Docker Compose.
- Every part should be implemented as simple as possible.
- The sensitive data such as alphavantage API key, should be passed from the .env


**Local development bootstrap**

1. Run ``$ make up-build`` or ``$ docker-compose.yml up -d --build``

**Links**

Swagger: http://localhost:8083/swagger/

Admin panel: http://localhost:8083/swagger/

**For checking**
1. Create superuser (for adding api key via admin panel)
2. Add api key (Table API keys in Admin panel)