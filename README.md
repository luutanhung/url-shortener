# 🚀 URL Shortener

![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)

URL Shortener takes a long, messy link and transforms it to a concise, elegant, and easy-to-share version.

## Table of Contents
- [Getting Started](#getting-started)
- [Requirements](#requirements)
- [Security Reports](#security-reports)
- [License](#license)
- [Authors](#authors)

## Getting Started

This project provides a simple URL Shortener. Below are the main API endpoints:

### Shorten URL [POST /api/shorten]
Creates a shortened version of the provided URL.

+ Request (application/json)

        {
            "url": "https://example.com"
        }

+ Response 201 (application/json)

        {
            "id": "1",
            "short_code": "abc123",
            "original_url": "https://example.com",
            "created_at": "2025-08-28T07:53:04Z"
        }

+ Response 400 (application/json)

        {
            "detail": "Invalid URL format"
        }

+ Response 500 (application/json)

        {
            "detail": "Failed to insert URL"
        }

### Redirect to Original URL [GET /{short_code}]

Redirects to the original URL based on the provided short code.

+ Parameters
    + short_code (string) - The shortened URL code

+ Response 302 (application/json)

        {
            "original_url": "https://example.com"
        }

+ Response 404 (application/json)

        {
            "detail": "Short URL not found"
        }

## Requirements
- **[Docker](https://www.docker.com/)** >= 24.0
- **[Docker Compose](https://docs.docker.com/compose/)** >= 2.0

System with at least **4GB RAM** (more recommended for smoother performance)

For detailed instructions on installing Docker and Docker Compose, you can visit the official documentation:
- Docker: [Get Started with Docker](https://www.docker.com/get-started)
- Docker Compose: [Overview of installing Docker Compose
](https://docs.docker.com/compose/install/)


## Installation
This project uses **Docker Compose** to simplify setup, so you don't need to install dependencies manually. The provided `docker-compose.yml` will:
1. Pull necessary Docker images.
2. Create and start all required services (database, backend, etc.).
3. Set up environment variables from a `.env` file.
After cloning the repository, simply run:
```bash
docker compose up -d
```


## Security Reports
Please send any security-related issues to <luutanhung.dev@gmail.com>. Thanks a lot.

## License
URL Shortener is distributed under the MIT License. See `License.md` for more details.

## Authors
- Lưu Tấn Hưng | [GitHub](https://github.com/luutanhung) | [X](https://x.com/luu_tan_hung) | <luutanhung.dev@gmail.com>
