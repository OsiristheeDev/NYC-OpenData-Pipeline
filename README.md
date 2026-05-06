NYC's Open Data Portal is a valuable resource for investigating traffic incidents in New York City, but it contains a vast amount of data on all the collisions and the people involved that have happened since 2012. As someone working to improve safety for cyclists, an underinvested group, I wanted to analyze specifically micro-mobility data.

Before I could do that though, I needed to extract, transform, and load the data into my own PostgreSQL database to analyze and plot for my map. Previously I had done that with just Pandas and CSVs, but since the NYPD updates the datasets daily the data source I was working with would quickly become out of date. I built this pipeline to keep cleaned data consistently flowing to my database and my cycling stress map.

**What the pipeline does:**
- **Extract** — pulls from two NYC Open Data Socrata APIs: the Motor Vehicle Collisions (Vehicles) dataset and the Persons dataset. Because the Persons API rejects large payloads, collision IDs are split into chunks of 80 and requested incrementally if over the threshold.
- **Transform** — consolidates the messy vehicle type codes in the source data (e.g. `'bike'`, `'Bicycle'`, `'BICYCLE'` all become `'Bike'`), combines the separate crash date and time columns into a single datetime, and cleans up nulls for safe database loading.
- **Load** — upserts cleaned records into PostgreSQL. On the very first run the pipeline creates all necessary tables automatically. On subsequent runs it checks whether it has already run today — if so, it exits without duplicating data.

**To Run This Yourself** You'll need an App Token for Socrata which you can obtain [here](https://dev.socrata.com/consumers/getting-started) and a PostgreSQL database to load the data to. Copy `.env.example`, fill in your database credentials and app token, then rename it to `.env`. Run `uv sync` to install all dependencies.

**Areas for Expansion:**
The initial run can be a bit slow and I suspect with a significant refactor it can run faster. Also since Socrata holds a lot of cities data I would like to add functionality to extract data from other cities collision datasets such as Chicago and L.A