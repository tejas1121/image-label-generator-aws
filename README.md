🖼️ Image Label Generator using AWS Rekognition

A fully serverless image labeling application built on AWS that allows users to upload images via a web interface and automatically retrieves AI-generated labels using Amazon Rekognition.

This project demonstrates event-driven architecture, secure image uploads using presigned URLs, and asynchronous processing with zero server management.

🚀 Features

Upload images directly from the browser

Secure uploads using S3 Presigned URLs

Automatic image analysis using Amazon Rekognition

Stores detected labels in Amazon DynamoDB

Fetches labels asynchronously via API

Fully serverless & scalable

Low cost, pay-per-use architecture

🧩 Architecture Overview
High-level flow:

User requests an upload URL

Image is uploaded directly to S3

S3 triggers Lambda for image analysis

Rekognition detects labels

Labels are stored in DynamoDB

Frontend polls API to fetch labels

User → S3 (Frontend)
   → API Gateway → Lambda (Presigned URL)
   → S3 Image Upload
   → Lambda (Triggered by S3)
   → Rekognition
   → DynamoDB
   → API Gateway → User


This design ensures scalability, security, and minimal operational overhead.

🛠 Tech Stack
Frontend

HTML

CSS

JavaScript

Hosted on Amazon S3 (Static Website Hosting)

Backend (Serverless)

Amazon API Gateway

AWS Lambda (Python 3.12)

Amazon S3

Amazon Rekognition

Amazon DynamoDB

IAM

📂 Project Structure
Image-Label-Generator/
│
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── app.js
│
├── lambda/
│   ├── generate_upload_url.py
│   ├── process_image_rekognition.py
│   └── get_image_labels.py
│
├── architecture/
│   └── architecture.png
│
└── README.md

🔐 Security Highlights

No AWS credentials exposed to frontend

Image uploads use temporary presigned URLs

IAM roles follow least privilege principle

Backend access controlled via API Gateway

💰 Cost Considerations

Free / near-zero cost when idle

Rekognition is charged only per image processed

Lambda, DynamoDB, and API Gateway stay within free tier for low usage

Suitable for portfolio and demo projects

🧪 How It Works (User Perspective)

Open the web app

Select an image

Click upload

Wait a few seconds

View detected labels with confidence scores

🎯 Learning Outcomes

This project demonstrates:

Serverless application design

Event-driven workflows

Secure cloud architecture

AWS AI service integration

Real-world frontend ↔ backend interaction

📌 Future Improvements

Support for video label detection

Authentication using Amazon Cognito

Label filtering & confidence thresholds

UI enhancements and animations

History page for uploaded images

👤 Author

Tejas Burkul
AWS | Cloud | Serverless Enthusiast

📌 GitHub: https://github.com/tejas1121

⭐ Acknowledgements

AWS Documentation

Amazon Rekognition API

AWS Serverless Architecture Patterns
