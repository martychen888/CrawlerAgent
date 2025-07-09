
#!/bin/bash

docker build -t chatcrawler-app .
docker run -d -p 7860:7860 --name chatcrawler chatcrawler-app
echo "ChatCrawler deployed at http://localhost:7860"
