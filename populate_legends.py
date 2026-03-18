import os
import django
import requests
from datetime import date
from io import BytesIO
import datetime
from django.core.files import File
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'F1StatsHub.settings')
django.setup()

from stats.models import Team, Driver, SeasonStats, RaceResult, RacePosition
from django.contrib.auth.models import User

# Hardcoded data for 14 Teams and 50 Drivers to ensure perfect reliability
TEAMS_DATA = [
    {'name': 'Ferrari', 'country': 'Italy', 'championships': 16, 'principal': 'Fred Vasseur', 'color': '#FF2800'},
    {'name': 'McLaren', 'country': 'United Kingdom', 'championships': 8, 'principal': 'Andrea Stella', 'color': '#FF8700'},
    {'name': 'Mercedes', 'country': 'Germany', 'championships': 8, 'principal': 'Toto Wolff', 'color': '#00D2BE'},
    {'name': 'Williams', 'country': 'United Kingdom', 'championships': 9, 'principal': 'James Vowles', 'color': '#005AFF'},
    {'name': 'Red Bull Racing', 'country': 'Austria', 'championships': 6, 'principal': 'Christian Horner', 'color': '#0600EF'},
    {'name': 'Team Lotus', 'country': 'United Kingdom', 'championships': 7, 'principal': 'Colin Chapman', 'color': '#FFB800'},
    {'name': 'Benetton', 'country': 'United Kingdom', 'championships': 1, 'principal': 'Flavio Briatore', 'color': '#00A382'},
    {'name': 'Brabham', 'country': 'United Kingdom', 'championships': 2, 'principal': 'Bernie Ecclestone', 'color': '#FFFFFF'},
    {'name': 'Tyrrell', 'country': 'United Kingdom', 'championships': 1, 'principal': 'Ken Tyrrell', 'color': '#004225'},
    {'name': 'Brawn GP', 'country': 'United Kingdom', 'championships': 1, 'principal': 'Ross Brawn', 'color': '#CEFF00'},
    {'name': 'Aston Martin', 'country': 'United Kingdom', 'championships': 0, 'principal': 'Mike Krack', 'color': '#006F62'},
    {'name': 'Alpine', 'country': 'France', 'championships': 2, 'principal': 'Bruno Famin', 'color': '#FF87BC'},
    {'name': 'Sauber', 'country': 'Switzerland', 'championships': 0, 'principal': 'Alessandro Alunni Bravi', 'color': '#00E701'},
    {'name': 'Haas', 'country': 'USA', 'championships': 0, 'principal': 'Ayao Komatsu', 'color': '#FFFFFF'},
]

# 50 Famous Drivers
DRIVERS_DATA = [
    ("Lewis Hamilton", "44", "British", "Mercedes", 7, 103, 197, 65, 4639.5, "1985-01-07"),
    ("Michael Schumacher", "1", "German", "Ferrari", 7, 91, 155, 77, 1566, "1969-01-03"),
    ("Max Verstappen", "1", "Dutch", "Red Bull Racing", 3, 54, 98, 30, 2586.5, "1997-09-30"),
    ("Alain Prost", "2", "French", "McLaren", 4, 51, 106, 41, 798.5, "1955-02-24"),
    ("Sebastian Vettel", "5", "German", "Red Bull Racing", 4, 53, 122, 38, 3098, "1987-07-03"),
    ("Ayrton Senna", "1", "Brazilian", "McLaren", 3, 41, 80, 19, 614, "1960-03-21"),
    ("Fernando Alonso", "14", "Spanish", "Aston Martin", 2, 32, 106, 24, 2267, "1981-07-29"),
    ("Nigel Mansell", "5", "British", "Williams", 1, 31, 59, 30, 482, "1953-08-08"),
    ("Jackie Stewart", "11", "British", "Tyrrell", 3, 27, 43, 15, 360, "1939-06-11"),
    ("Jim Clark", "1", "British", "Team Lotus", 2, 25, 32, 28, 274, "1936-03-04"),
    ("Niki Lauda", "1", "Austrian", "Ferrari", 3, 25, 54, 24, 420.5, "1949-02-22"),
    ("Juan Manuel Fangio", "1", "Argentine", "Mercedes", 5, 24, 35, 23, 277.64, "1911-06-24"),
    ("Nelson Piquet", "5", "Brazilian", "Brabham", 3, 23, 60, 23, 485.5, "1952-08-17"),
    ("Nico Rosberg", "6", "German", "Mercedes", 1, 23, 57, 20, 1594.5, "1985-06-27"),
    ("Damon Hill", "0", "British", "Williams", 1, 22, 42, 19, 360, "1960-09-17"),
    ("Kimi Räikkönen", "7", "Finnish", "Ferrari", 1, 21, 103, 46, 1873, "1979-10-17"),
    ("Mika Häkkinen", "1", "Finnish", "McLaren", 2, 20, 51, 25, 420, "1968-09-28"),
    ("Stirling Moss", "7", "British", "Mercedes", 0, 16, 24, 19, 185.64, "1929-09-17"),
    ("Jenson Button", "22", "British", "Brawn GP", 1, 15, 50, 8, 1235, "1980-01-19"),
    ("Graham Hill", "1", "British", "Team Lotus", 2, 14, 36, 10, 289, "1929-02-15"),
    ("Jack Brabham", "1", "Australian", "Brabham", 3, 14, 31, 12, 261, "1926-04-02"),
    ("Emerson Fittipaldi", "1", "Brazilian", "McLaren", 2, 14, 35, 6, 281, "1946-12-12"),
    ("Alberto Ascari", "1", "Italian", "Ferrari", 2, 13, 17, 12, 140.14, "1918-07-13"),
    ("David Coulthard", "2", "British", "McLaren", 0, 13, 62, 18, 535, "1971-03-27"),
    ("Mario Andretti", "5", "American", "Team Lotus", 1, 12, 19, 10, 180, "1940-02-28"),
    ("Carlos Reutemann", "2", "Argentine", "Williams", 0, 12, 45, 6, 310, "1942-04-12"),
    ("Alan Jones", "27", "Australian", "Williams", 1, 12, 24, 13, 206, "1946-11-02"),
    ("Jacques Villeneuve", "3", "Canadian", "Williams", 1, 11, 23, 9, 235, "1971-04-09"),
    ("Felipe Massa", "19", "Brazilian", "Ferrari", 0, 11, 41, 15, 1167, "1981-04-25"),
    ("Rubens Barrichello", "2", "Brazilian", "Ferrari", 0, 11, 68, 17, 658, "1972-05-23"),
    ("Ronnie Peterson", "1", "Swedish", "Team Lotus", 0, 10, 26, 9, 206, "1944-02-14"),
    ("Jody Scheckter", "11", "South African", "Ferrari", 1, 10, 33, 5, 255, "1950-01-29"),
    ("James Hunt", "1", "British", "McLaren", 1, 10, 14, 8, 222, "1947-08-29"),
    ("Valtteri Bottas", "77", "Finnish", "Mercedes", 0, 10, 67, 19, 1797, "1989-08-28"),
    ("Mark Webber", "2", "Australian", "Red Bull Racing", 0, 9, 42, 19, 1047.5, "1976-08-27"),
    ("Daniel Ricciardo", "3", "Australian", "Red Bull Racing", 0, 8, 32, 16, 1311, "1989-07-01"),
    ("René Arnoux", "16", "French", "Ferrari", 0, 7, 22, 12, 181, "1948-07-04"),
    ("Juan Pablo Montoya", "2", "Colombian", "Williams", 0, 7, 30, 12, 307, "1975-09-20"),
    ("Denis Hulme", "1", "New Zealander", "McLaren", 1, 8, 33, 9, 248, "1936-06-18"),
    ("Charles Leclerc", "16", "Monegasque", "Ferrari", 0, 5, 30, 7, 1074, "1997-10-16"),
    ("Sergio Perez", "11", "Mexican", "Red Bull Racing", 0, 6, 35, 11, 1486, "1990-01-26"),
    ("George Russell", "63", "British", "Mercedes", 0, 1, 11, 6, 469, "1998-02-15"),
    ("Carlos Sainz", "55", "Spanish", "Ferrari", 0, 2, 18, 3, 982.5, "1994-09-01"),
    ("Lando Norris", "4", "British", "McLaren", 0, 0, 13, 6, 633, "1999-11-13"),
    ("Pierre Gasly", "10", "French", "Alpine", 0, 1, 4, 3, 394, "1996-02-07"),
    ("Esteban Ocon", "31", "French", "Alpine", 0, 1, 3, 0, 422, "1996-09-17"),
    ("Keke Rosberg", "6", "Finnish", "Williams", 1, 5, 17, 3, 159.5, "1948-12-06"),
    ("Gilles Villeneuve", "27", "Canadian", "Ferrari", 0, 6, 13, 8, 101, "1950-01-18"),
    ("Jacky Ickx", "1", "Belgian", "Ferrari", 0, 8, 25, 14, 181, "1945-01-01"),
    ("Riccardo Patrese", "6", "Italian", "Williams", 0, 6, 37, 13, 281, "1954-04-17")
]

def fetch_ergast_races():
    # Attempt to use Ergast API to fetch current season race results
    print("Attempting to fetch latest 2023 race results from Ergast API...")
    try:
        response = requests.get('http://ergast.com/api/f1/2023/results/1.json')
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"API Fetch failed: {e}")
    return None

def populate():
    # Clear existing
    Driver.objects.all().delete()
    Team.objects.all().delete()
    RaceResult.objects.all().delete()
    SeasonStats.objects.all().delete()
    
    # Create User
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin')

    team_map = {}
    for td in TEAMS_DATA:
        t = Team.objects.create(
            name=td['name'],
            country=td['country'],
            championships=td['championships'],
            team_principal=td['principal'],
            color=td['color']
        )
        team_map[td['name']] = t
        
    driver_map = {}
    for d in DRIVERS_DATA:
        d_team = team_map.get(d[3])
        driver = Driver.objects.create(
            name=d[0],
            number=d[1],
            nationality=d[2],
            team=d_team,
            championships=d[4],
            wins=d[5],
            podiums=d[6],
            fastest_laps=d[7],
            career_points=d[8],
            date_of_birth=datetime.datetime.strptime(d[9], "%Y-%m-%d").date()
        )
        driver_map[d[0]] = driver
        
        # Add a mock historical season stats
        SeasonStats.objects.create(
            driver=driver,
            year=2020 if d[4] == 0 else 1995,
            team=d_team,
            races=20,
            wins=d[5] // 10,
            podiums=d[6] // 8,
            points=d[8] / 15,
            championship_position=1 if d[4] > 0 else 5
        )

    print(f"Created {len(team_map)} Teams and {len(driver_map)} Drivers")
    print("Ergast API interaction starting...")
    api_data = fetch_ergast_races()

    if api_data and 'MRData' in api_data:
        races = api_data['MRData']['RaceTable']['Races']
        for r in races[:5]: # Take first 5 winning positions logged from api
            try:
                race_obj = RaceResult.objects.create(
                    race_name=r['raceName'],
                    circuit=r['Circuit']['circuitName'],
                    country=r['Circuit']['Location']['country'],
                    race_date=datetime.datetime.strptime(r['date'], "%Y-%m-%d").date()
                )
                res = r['Results'][0]
                driver_name = f"{res['Driver']['givenName']} {res['Driver']['familyName']}"
                driver_obj = Driver.objects.filter(name__icontains=res['Driver']['familyName']).first()
                if driver_obj:
                    RacePosition.objects.create(
                        race=race_obj,
                        driver=driver_obj,
                        team=driver_obj.team,
                        position=1,
                        points=float(res['points']),
                        race_time=res.get('Time', {}).get('time', 'Finished')
                    )
            except Exception as e:
                print(f"Failed parsing race: {e}")
    else:
        # Fallback Mock Race if API disabled
        print("Using Fallback Race Data since Ergast API blocked/down")
        r1 = RaceResult.objects.create(
            race_name="Monaco Grand Prix",
            circuit="Circuit de Monaco",
            country="Monaco",
            race_date=datetime.date(2023, 5, 28)
        )
        max_v = driver_map.get("Max Verstappen")
        alonso = driver_map.get("Fernando Alonso")
        ocon = driver_map.get("Esteban Ocon")
        
        if max_v:
            RacePosition.objects.create(race=r1, driver=max_v, team=max_v.team, position=1, points=25, race_time="1:48:51.980")
        if alonso:
            RacePosition.objects.create(race=r1, driver=alonso, team=alonso.team, position=2, points=18, race_time="+27.921s")
        if ocon:
            RacePosition.objects.create(race=r1, driver=ocon, team=ocon.team, position=3, points=15, race_time="+36.990s")

    print("Population and API caching complete")

if __name__ == '__main__':
    populate()
