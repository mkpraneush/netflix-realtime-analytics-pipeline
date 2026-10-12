# Netflix Real-Time Analytics Pipeline

A near real-time data analytics pipeline built on Netflix titles data. Raw CSV files are cleaned with **Python & Pandas**, stored in **MySQL**, analysed with **SQL**, kept fresh through **scheduled automation**, and visualised in a live **Power BI** dashboard using **DirectQuery**.

> **Note:** "Real-time" here means near real-time. A scheduler polls for new data every few minutes and inserts it into MySQL. It is not event-driven streaming.

---

## Architecture

```
Netflix CSV files ──► Python (Pandas cleaning) ──► MySQL (netflix_analytics)
                                                        ▲        │
 API / simulated new data ──► automation.py ────────────┘        ▼
        (runs every few minutes)                    SQL analytics + views
                                                                 │
                                                                 ▼
                                                  Power BI (DirectQuery)
```

## Tech Stack

| Layer | Tools |
|---|---|
| Language | Python 3.11 |
| Data cleaning | Pandas |
| Database | MySQL (`mysql-connector-python`) |
| Analytics | SQL (queries and views) |
| Automation | Python scheduler |
| Visualisation | Power BI (DirectQuery) |

## Dataset

- **5,850 titles**: 3,744 movies (64%) and 2,106 shows (36%)
- Two tables: `titles` (title details, type, release year, IMDb score and votes) and `credits` (cast and crew)

---

## Project Structure

```
Real_Time_Netflix_Data_Project/
├── data/
│   ├── titles.csv / credits.csv                 # raw data
│   └── titles_cleaned.csv / credits_cleaned.csv # cleaned data
├── sql/
│   └── views.sql          # SQL views used by Power BI
├── config.py              # settings loaded from .env
├── data_cleaning.py       # Pandas cleaning script
├── database.py            # MySQL connection, table creation, inserts
├── sql_operations.py      # SQL analytics functions
├── api_data.py            # fetches new data for the live feed
├── automation.py          # scheduler that runs the pipeline repeatedly
├── test_csv.py            # quick check that CSVs load correctly
├── requirements.txt
└── .env.example           # template for credentials
```

---

## 1. What I Did in Python

### Data cleaning (`data_cleaning.py`)
- Loaded the raw `titles.csv` and `credits.csv` with Pandas
- Handled missing values and duplicate records
- Fixed data types (years, scores, votes)
- Saved the results as `titles_cleaned.csv` and `credits_cleaned.csv`

### Database loading (`database.py`)
- Connected Python to MySQL with `mysql-connector-python`
- Created the `netflix_analytics` database and the `titles` and `credits` tables
- Inserted the cleaned data into MySQL

### Analytics functions (`sql_operations.py`)
Python functions that run SQL queries and print the results:

- `create_connection()`: opens the MySQL connection
- `total_content()`: total number of titles
- `content_by_type()`: movies vs shows
- `content_percentage()`: percentage split of movies and shows
- `data_quality_audit()`: checks fields for invalid or missing values
- `content_by_year()`: titles released per year
- `average_imdb_score()`: average IMDb rating

### Live data and automation (`api_data.py`, `automation.py`)
- `api_data.py` fetches new records
- `automation.py` runs the fetch-and-insert job on a schedule so the table keeps growing without manual work
- Duplicate inserts are avoided by using a unique key on each title

---

## 2. What I Did in MySQL

- Designed the `netflix_analytics` database with two tables: `titles` and `credits`
- Set up a primary key on the title ID so repeated runs do not create duplicate rows
- Wrote SQL queries for:
  - Total content count
  - Movies vs shows (count and percentage)
  - Titles released by year
  - Average IMDb score
  - Data quality checks (nulls and invalid values)
- Created **SQL views** in `sql/views.sql` so Power BI reads clean, ready-to-use data

> Sample query:
> ```sql
> SELECT type, COUNT(*) AS total
> FROM titles
> GROUP BY type;
> ```

---

## 3. What I Did in Power BI

- Connected Power BI to the MySQL `netflix_analytics` database
- Used **DirectQuery** mode, so the dashboard reads directly from MySQL and shows new rows after a refresh without re-importing data
- Built visuals on top of the SQL views, such as:
  - KPI cards (total titles, average IMDb score)
  - Movies vs shows split
  - Titles released per year
  - Top-rated content

*(Edit this list to match the visuals in your final dashboard.)*

### Dashboard Preview
> Add screenshots here: `![Dashboard](images/dashboard.png)`

---

## How to Run

```bash
# 1. Clone the repository
git clone https://github.com/mkpraneush/netflix-realtime-analytics-pipeline.git
cd netflix-realtime-analytics-pipeline

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up credentials: copy .env.example to .env and fill in your MySQL details

# 4. Clean the data
python data_cleaning.py

# 5. Create the tables and load data
python database.py

# 6. Run analytics
python sql_operations.py

# 7. Start the automated pipeline
python automation.py
```

Then open Power BI, connect to MySQL in **DirectQuery** mode, and load the views.

---

## Future Improvements

- Replace polling with a message queue or streaming tool (for example Kafka) for true real-time ingestion
- Add logging and retry handling to the automation script
- Containerise the project with Docker
- Add automated tests

---

## Author

**Praneush**: B.Tech Information Technology
GitHub: [mkpraneush](https://github.com/mkpraneush)
