# Archus Framework
Archus is a lightweight and modular Python web framework designed to be simple yet powerful and based on <b>wsgi</b>. It allows developers to quickly build web applications with minimal setup. Archus supports middleware, templating, and routing out of the box, making it an excellent choice for both small and large web projects.

## Features
- **Middleware Support**: Easily add and manage middleware components.
- **Routing**: Simple and flexible routing system.
- **Templating**: Jinja2 templating engine for dynamic HTML generation.
- **Static and Media Files Handling**: Serve static and media files effortlessly.
- **CORS and Security Headers**: Built-in support for CORS and security headers.
- **Global Exception Handling**: Graceful handling of exceptions.
- **Rest Api Support**: It supports rest api designing with proper versioning.
- **Serializer**: Built in <b>ArchusSerializer</b> helps to serialize, deserialize and validate your json api data.
- **ArchusException**: Built in <b>ArchusException</b> allows you to throw a custom exception which is handled by <b>Global Exception Handler</b>.

## Installation
Install Archus via pip:

```sh
pip install archus
```

## Create Your First Project
```sh
archus createproject [your_project]
```

## After create project
```sh
cd [your_project]
python3 run.py
```

## Documentation available at `/docs`
`Example: http://localhost:8000/docs`
