# home-db
home-db is an AWS backed cloud environment to assist in home automation. Utilizing RDS, Lambda, and API Gateway, home-db exposes API endpoints for sensors and other IoT devices to store data.

## Installation
This document is not meant to serve as an exhaustive guide to setting up the home-db, instead it provides a high-level overview of the required steps to stand up home-db.

### RDS
1. Launch MySQL RDS Instance
2. Execute `home-db.sql`

### Lambda

1. Zip the contents of the `lambda` directory
2. Upload to the applicable Lambda function in AWS