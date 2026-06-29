# GeoJSON Dashboard

A Streamlit-based web dashboard for internal GIS teams to upload, visualize, validate, and clean GeoJSON farm polygon data, supporting EUDR compliance workflows.

## Project Structure

```text
automation/
├── src/
│   ├── web_app.py          # Main Streamlit interface
│   ├── geometry_utils.py   # Geometry validation and repair utilities
│   ├── file_handler.py     # GeoJSON loading and processing
│   ├── ai_assistant.py     # Gemini AI integration
│   └── logger.py           # Logging configuration
│
├── data/                   # Sample datasets
├── Dockerfile              # Docker deployment configuration
└── requirements.txt        # Project dependencies
```

---

## Features
- Upload GeoJSON/JSON files
- Interactive table with attribute editing
- Interactive map visualization using Folium/Leaflet
- Automatic duplicate geometry detection and removal
- Invalid geometry detection, reporting, and automated fixing
- AI assistant (Gemini) for natural language data queries
- Download cleaned GeoJSON
- Error logging

## Run Locally
```bash
git clone <your-repo>
cd automation
pip install -r requirements.txt
cd src
streamlit run web_app.py
```

## Run with Docker
```bash
docker build -t geojson-dashboard .
docker run -p 8501:8501 geojson-dashboard
```
Then open http://localhost:8501 in your browser.

## Export Docker Image
```bash
docker save -o geojson-dashboard.tar geojson-dashboard
```

## Tech Stack
- Python, Streamlit, GeoPandas, Shapely, Folium, streamlit-folium
- Google Gemini API (AI assistant)
- Docker

## Notes
- Gemini API key required in `src/ai_assistant.py`
- Docker build requires internet access to pull base images
