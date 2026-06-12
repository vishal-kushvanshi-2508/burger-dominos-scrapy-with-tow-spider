# Burger & Dominos Data Scraper Using Scrapy

## 📖 Overview

This project is a Python-based web scraping solution developed using Scrapy to extract restaurant-related information from Burger King and Dominos websites. The project contains two separate spiders designed to collect structured data efficiently and export it into a usable format.

The project demonstrates practical experience in Scrapy spider development, XPath extraction, multi-spider architecture, and structured data processing.

---

## 🚀 Features

- Multi-spider Scrapy project
- Automated data extraction
- Structured JSON output
- XPath-based parsing
- Error handling and logging
- Scalable scraping architecture
- Clean and maintainable codebase

---

## 🛠️ Technologies Used

- Python
- Scrapy
- XPath
- JSON
- Logging

---

## 📊 Extracted Data

- Restaurant Name
- Store URL
- Address
- City
- State
- Postal Code
- Contact Information
- Additional Restaurant Details

---

## 📁 Project Structure

```text
burger-dominos-scrapy-with-tow-spider/
│
├── scrapy.cfg
├── requirements.txt
├── README.md
│
└── burger_dominos/
    │
    ├── __init__.py
    ├── items.py
    ├── pipelines.py
    ├── settings.py
    │
    └── spiders/
        │
        ├── __init__.py
        ├── burger_spider.py
        └── dominos_spider.py
```

---

## ⚡ Installation

```bash
pip install -r requirements.txt
```

---

## ▶️ Run Burger Spider

```bash
scrapy crawl burger_spider
```

---

## ▶️ Run Dominos Spider

```bash
scrapy crawl dominos_spider
```

---

## 📂 Export Output

### Burger Data

```bash
scrapy crawl burger_spider -o burger_data.json
```

### Dominos Data

```bash
scrapy crawl dominos_spider -o dominos_data.json
```

---

## 🎯 Learning Outcomes

- Scrapy Framework
- Multi-Spider Project Architecture
- XPath Data Extraction
- JSON Data Processing
- Spider Development
- Error Handling and Logging
- Scalable Web Scraping Solutions

---

### 🔗 GitHub Profiles

💼 Professional Work  
https://github.com/vishal-kushvanshi-2508

📚 Practice Projects & Learning  
https://github.com/vishal-2508
