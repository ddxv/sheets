# Sheety

Sheety is a simple wrapper around Gspread that simplifies it's handling of Pandas dataframes. It also accepts CSV files which can created / called from R.

It was developed at Bubbleye for quick and dirty projects so watch out for rough edges. If you have any questions please feel free to reach out.


## Getting Started

1. On Google Developer Console create a project + enable Drive and Sheets APIs
2. Create a service account with "Editor" priviledges and download Google API credentials in ~/auth/sheety-credentials.json
2. Share your destination sheet with the email located near the bottom of your sheety-credentials.json 
3. Download and `pip install -e .`

### Prerequisites

Requirements:

```
gspread
pandas
oauth2client
```

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


