# Serverless Image Processing with S3 and Lambda

## Project Overview
This project implements a **serverless image processing application** where users upload images to an S3 bucket, which triggers an AWS Lambda function that processes the images (resize, watermark) and stores them in another S3 bucket.

### Key AWS Services
- **Amazon S3**: Stores original and processed images.
- **AWS Lambda**: Executes image processing logic.
- **Optional EC2/Flask Imgproxy**: Handles advanced image processing if needed.

---

## Architecture Diagram
![Architecture Diagram](architecture-diagram.png)

**Description:**
1. **User uploads image** → S3 Source Bucket.
2. **S3 triggers Lambda** → Lambda retrieves the image.
3. **Image is processed** → Resized and Watermarked.
4. **Processed image uploaded** → S3 Destination Bucket.
5. **Optional**: Imgproxy on EC2 can handle processing if Lambda lacks required libraries.

---

## Project Structure
