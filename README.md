Spotalyze

Overview
This project is designed to analyze trends in music popularity by extracting data from the Spotify API, processing it, and analyzing it to identify which artists are most commonly played each month. The pipeline integrates with Snowflake for data storage and Databricks for data analysis, offering insights into the evolving music landscape.

Getting Started
To get started with this project, follow these steps:

Prerequisites
Ensure you have Python installed on your machine. This project requires Python 3.6 or newer.

Installation
Clone the Repository
Clone this repository to your local machine using Git. If you don't have Git installed, download and install it from git-scm.com.

git clone https://github.com/yourusername/spotify_trends_analysis.git
cd spotify_trends_analysis
Set Up a Virtual Environment
Navigate to the project directory and create a new virtual environment. Activate it using the following commands:

On Windows:
.venv\Scripts\activate
On macOS/Linux:
source.venv/bin/activate
Install Dependencies
Install the required Python packages by running:

pip install requests pandas snowflake-connector-python
Usage
Obtain Spotify API Credentials
To access the Spotify API, you'll need to register your application on the Spotify Developer Dashboard and obtain your client ID and secret.

Configure the Project
Update the spotify_api/api_handler.py file with your Spotify client ID and secret.

Run the Pipeline
Execute the main script or module responsible for running the pipeline. This will typically involve calling a function or class method that orchestrates the data extraction, processing, and analysis stages.

Contributing
Contributions are welcome Please feel free to submit pull requests or open issues for discussion.
