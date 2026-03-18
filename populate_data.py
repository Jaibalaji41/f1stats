import os
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'F1StatsHub.settings')
django.setup()

from stats.models import Team, Driver, Race, SeasonStats
from django.contrib.auth.models import User

def populate():
    # Create superuser
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin')

    # Create Teams
    mercedes, _ = Team.objects.get_or_create(
        name='Mercedes', 
        country='Germany', 
        team_principal='Toto Wolff', 
        championships=8
    )
    red_bull, _ = Team.objects.get_or_create(
        name='Red Bull Racing', 
        country='Austria', 
        team_principal='Christian Horner', 
        championships=6
    )
    ferrari, _ = Team.objects.get_or_create(
        name='Ferrari', 
        country='Italy', 
        team_principal='Fred Vasseur', 
        championships=16
    )
    mclaren, _ = Team.objects.get_or_create(
        name='McLaren', 
        country='United Kingdom', 
        team_principal='Andrea Stella', 
        championships=8
    )

    # Create Drivers
    hamilton, _ = Driver.objects.get_or_create(
        name='Lewis Hamilton',
        team=mercedes,
        country='United Kingdom',
        number=44,
        championships=7,
        wins=103,
        podiums=197,
        points=4639.5
    )
    verstappen, _ = Driver.objects.get_or_create(
        name='Max Verstappen',
        team=red_bull,
        country='Netherlands',
        number=1,
        championships=3,
        wins=54,
        podiums=98,
        points=2586.5
    )
    leclerc, _ = Driver.objects.get_or_create(
        name='Charles Leclerc',
        team=ferrari,
        country='Monaco',
        number=16,
        championships=0,
        wins=5,
        podiums=30,
        points=1074.0
    )
    norris, _ = Driver.objects.get_or_create(
        name='Lando Norris',
        team=mclaren,
        country='United Kingdom',
        number=4,
        championships=0,
        wins=0,
        podiums=13,
        points=633.0
    )

    # Create Races
    r1, _ = Race.objects.get_or_create(
        race_name='Bahrain Grand Prix',
        circuit_name='Bahrain International Circuit',
        country='Bahrain',
        race_date=date(2024, 3, 2),
        winner=verstappen,
        team=red_bull
    )
    r2, _ = Race.objects.get_or_create(
        race_name='Saudi Arabian Grand Prix',
        circuit_name='Jeddah Corniche Circuit',
        country='Saudi Arabia',
        race_date=date(2024, 3, 9),
        winner=verstappen,
        team=red_bull
    )
    r3, _ = Race.objects.get_or_create(
        race_name='Australian Grand Prix',
        circuit_name='Albert Park Circuit',
        country='Australia',
        race_date=date(2024, 3, 24),
        winner=leclerc,
        team=ferrari
    )

    # Create Season Stats for 2023
    SeasonStats.objects.get_or_create(
        year=2023, driver=verstappen, team=red_bull, races=22, wins=19, podiums=21, points=575, position=1
    )
    SeasonStats.objects.get_or_create(
        year=2023, driver=hamilton, team=mercedes, races=22, wins=0, podiums=6, points=234, position=3
    )
    SeasonStats.objects.get_or_create(
        year=2023, driver=leclerc, team=ferrari, races=22, wins=0, podiums=6, points=206, position=5
    )
    SeasonStats.objects.get_or_create(
        year=2023, driver=norris, team=mclaren, races=22, wins=0, podiums=7, points=205, position=6
    )

    print("Successfully populated data")

if __name__ == '__main__':
    populate()
