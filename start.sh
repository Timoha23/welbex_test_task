#!/bin/sh
echo "start migrate"
alembic upgrade head
echo "end migrate"
echo "start fill_locations"
python3 app/fillers/fill_locations.py
echo "end fill_locations"
echo "start fill_cars"
python3 app/fillers/fill_cars.py
echo "end fill_cars"
"$@"