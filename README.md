# Salesforce Data Cleaner Microservice

A small Python Flask microservice that:
- Accepts raw records (JSON array or CSV placed under `data/`)
- Cleans and normalizes fields (Name, Phone, Website)
- Optionally uploads cleaned records to Salesforce via the REST API
- Works in **mock** mode by default so you can demo without Salesforce credentials

## Features
- `POST /clean_and_upload` endpoint
- Accepts `{ "records": [...] }` or `{ "csv_path": "raw_accounts.csv" }`
- Cleans data and writes cleaned JSON to `cleaned/` when run in mock mode
- Example files included in `data/`

## Quickstart (local)

1. Clone or download this repo.
2. Create and activate a Python virtualenv (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Run the app (mock mode by default):
   ```bash
   export MOCK=true
   python app.py
   ```
4. Demo with sample JSON:
   ```bash
   curl -X POST http://localhost:5000/clean_and_upload \
     -H "Content-Type: application/json" \
     -d @data/demo_data.json
   ```

## Integrating with Salesforce (non-mock mode)

To push cleaned records to Salesforce set these environment variables:
- `MOCK=false`
- `SF_INSTANCE_URL` (e.g. `https://your-org.my.salesforce.com`)
- `SF_ACCESS_TOKEN` (OAuth access token)

> For production use you should implement an OAuth 2.0 flow (Web Server or JWT Bearer)
> and never store client secrets or access tokens directly in source control.

## CSV input

Place a CSV file under `data/` (header example: `Name,Phone,Website`) and call:
```bash
curl -X POST http://localhost:5000/clean_and_upload \
  -H "Content-Type: application/json" \
  -d '{"csv_path":"raw_accounts.csv"}'
```

## Next steps & enhancements
- Add batching and use Salesforce Composite or Bulk API for large volumes
- Add retries and exponential backoff for transient errors
- Add unit tests and Dockerfile for deployment
- Add authentication to the Flask endpoint if exposing publicly

-- End of README
