# frome-assignment

## Introduction

You are tasked with building a comprehensive RESTful API for a social media analytics platform. This API should provide various endpoints to analyze and retrieve data from any social media platform, with Twitter being the ideal focus. The API should allow users to retrieve insights, trends, and statistics about hashtags or any keywords.

## Endpoints

1. **Retrieve Posts Endpoint**
   - Description: Endpoint to retrieve posts based on a specific hashtag or keyword.
   - Output Format: JSON (Keys and Values)
   - Example Output:
     ```json
     {
        "id": {
            "data": "..."
        },
        "id": {
            "data": "..."
        }
     }
     ```

2. **Trends Analysis Endpoint**
   - Description: Endpoint to analyze trends and generate insights based on hashtag data.
   - Example Output:
     ```json
     {
        "good": 2,
        "bad": 0,
        "better": 5
     }
     ```
   - Note: This is just an example; analysis can be extended to various metrics such as sentiment analysis.

## Data Storage

Store social media data in a relational database - PostgreSQL.

## Deployment

Deploy the API server to a cloud service provider like AWS using Docker.

## Documentation

- Document all API endpoints, requirements text, and instructions to run and deploy the API.
- Create a GitHub repo, push everything to the repo, and update us.
