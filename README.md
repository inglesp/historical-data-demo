# historical-data-demo

This is a demo of how we could import data from historical releases into Gorgonzola.

We just show data about practices.
The basic idea is that we add a "release_date" column to the practice table.
So instead of having one row in the practice table for each practice, we have one row for each time a practice appears in a release file.

Then when showing the list of practices, we only show the rows that correspond to the latest release for each practice.

And when we show a single practice, by default we show the row that corresponds to the last release that had data for that practice.
But if the URL for the practice page contains a release_date query parameter, we instead show the row that correponds to the release .

## Set up

This is a vanilla Django app.
In a new virtualenv, run `pip install -r requirements.prod.txt`.

You can then run management commands, including `./manage.py migrate` to create a database.

There's some sample data in the data directory.

You can import it with eg:

    ./manage.py import_practices data/practices-20240101.csv
