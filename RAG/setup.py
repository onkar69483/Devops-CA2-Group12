from setuptools import setup, find_packages

setup(
    name="RAG Framework Chatbot",
    version="0.1.0",
    packages=find_packages(include=["app", "app.*",
                                    "input_layer", "input_layer.*",
                                    "config", "config.*",
                                    "retrieval_layer", "retrieval_layer.*",
                                    "storage_layer", "storage_layer.*"]),  # Specify the source directory
    package_dir={'': '.'},        # Map package to the src directory
    install_requires=[
        'fastapi==0.115.7', 
        'uvicorn==0.34.0',  
        'beautifulsoup4==4.13.3',
        'transformers==4.48.1', 
        'torch==2.5.1', 
        'groq==0.15.0',  
        'pyfiglet==1.0.2',
        'python-multipart==0.0.20',
        'langchain==0.3.18',
        'langchain-community==0.3.17',
        'sentence-transformers==3.4.1',
        'psycopg2-binary==2.9.10',
        'opensearch-py==2.8.0',
        'numpy==1.26.4',
        'pydantic==2.10.6',
        'requests==2.32.3',
        'PyMuPDF==1.25.3',
        'colorama==0.4.6'
    ],
    entry_points={
        'console_scripts': [
            'realtime_va=app.run:main',
        ],
    },
    description="This project integrates with a chatbot to provide an AI-powered query resolution system. It processes user queries with NLP techniques, and retrieves relevant documents from RAG to deliver precise responses directly.",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9.0',  # Specify the Python versions you support
    include_package_data=True,
    package_data={
        "storage_layer": ["*.pdf", "*.txt"],  # Include PDFs and TXT files
    }
)