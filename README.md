# Fibre - Scraper for current and upcoming albums

A Python based web scraper for extracting album data from albumoftheyear.org, which collects both currently released albums and upcoming (soon to be released) albums.

## Hierarchy (Structure)

```
Fibre/
├── README.md                    
├── main.py                      
├── requirements.txt     
├── scraper.log (will be created once run)                          
└── kaggle/
    └── data/
        ├── upcoming_albums.json (will be filled once run) 
        └── current_albums.json (will be filled once run)
```

## Features

- Collects information on both upcoming releases and current releases
- Automatically detects when pages start repeating to avoid duplicated data entries
- Built-in delays for rate limiting
- Logging, error handling
- JSON Output Files
- Kaggle integration

## Installation

### Prerequisites
- Python 3.6+

### Setup

1. **Clone or download the project files**
   ```bash
   cd /path/to/Fibre
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Enter your own information in ```dataset-metadata.json```**

4. **Setup API Keys**


## Usage

### Running Scraper
```bash
python main.py
```

### What it does:
1. Scrapes all pages from `/upcoming/` until duplicates are detected
2. Scrapes up to 50 pages from `/releases/`
3. Saves results to `kaggle/data/upcoming_albums.json` and `kaggle/data/current_albums.json` respectively
4. Logs in `scraper.log`

## Data Structure

Each album record contains:
```json
{
  "artist": "Artist Name",
  "album": "Album Title", 
  "date": "Release Date",
  "link": "https://albumoftheyear.org/album/...",
  "image": "https://cdn.albumoftheyear.org/..."
}
```

## Dependencies

- **requests**
- **beautifulsoup4**
- **json**
- **time**
- **logging**

## Error Handling

- Automatic retry and graceful failure if network error happens
- Default values for incomplete data entries
- Error logging

## Logging

All activities are logged to `scraper.log` with timestamps:
- Page requests
- Page responses
- Progress on scraping
- Errors
- File saves

## Performance

- ~3 requests per second
- 1000+ albums per run