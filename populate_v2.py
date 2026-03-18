import os
import django
import requests
from datetime import date
from io import BytesIO
from django.core.files import File

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'F1StatsHub.settings')
django.setup()

from stats.models import Team, Driver, Race, SeasonStats
from django.contrib.auth.models import User

# Stable image URLs for simulation
DRIVER_IMAGES = {
    'Lewis Hamilton': 'https://upload.wikimedia.org/wikipedia/commons/1/18/Lewis_Hamilton_2016_Malaysia_2.jpg',
    'Max Verstappen': 'https://upload.wikimedia.org/wikipedia/commons/7/75/Max_Verstappen_2017_Malaysia_3.jpg',
    'Charles Leclerc': 'https://upload.wikimedia.org/wikipedia/commons/2/23/F1_2019_Hockenheimring_-_Leclerc_%2848417743606%29.jpg',
    'Lando Norris': 'https://upload.wikimedia.org/wikipedia/commons/1/1e/FIA_F1_Austria_2019_Nr._4_Norris_2.jpg',
    'Fernando Alonso': 'https://upload.wikimedia.org/wikipedia/commons/4/4b/Fernando_Alonso_2017_Malaysia_2.jpg',
    'George Russell': 'https://upload.wikimedia.org/wikipedia/commons/2/27/FIA_F1_Austria_2019_Nr._63_Russell.jpg',
    'Carlos Sainz': 'https://upload.wikimedia.org/wikipedia/commons/1/1c/Carlos_Sainz_Jr._2019.jpg',
    'Sergio Perez': 'https://upload.wikimedia.org/wikipedia/commons/e/ea/F1_2019_Hockenheimring_-_Perez_%2848417616641%29.jpg'
}

TEAM_LOGOS = {
    'Mercedes': 'https://upload.wikimedia.org/wikipedia/commons/archive/f/fb/20160216122639%21Mercedes_AMG_Petronas_F1_Logo.svg',
    'Red Bull Racing': 'https://upload.wikimedia.org/wikipedia/en/thumb/8/87/Red_Bull_Racing_logo.svg/1024px-Red_Bull_Racing_logo.svg.png',
    'Ferrari': 'https://upload.wikimedia.org/wikipedia/en/thumb/c/c0/Scuderia_Ferrari_Logo.svg/1024px-Scuderia_Ferrari_Logo.svg.png',
    'McLaren': 'https://upload.wikimedia.org/wikipedia/en/thumb/6/66/McLaren_Racing_logo.svg/1024px-McLaren_Racing_logo.svg.png',
    'Aston Martin': 'https://upload.wikimedia.org/wikipedia/en/thumb/e/ef/Aston_Martin_Aramco_Cognizant_F1_Team_logo.svg/1024px-Aston_Martin_Aramco_Cognizant_F1_Team_logo.svg.png',
    'Alpine': 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Alpine_F1_Team_Logo.svg/1024px-Alpine_F1_Team_Logo.svg.png'
}

def get_image(url, filename):
    try:
        if url.endswith('.svg'):
            # SVG can't be handled by Pillow well easily, use placeholder
            response = requests.get('https://placehold.co/400x200/000000/FFFFFF/png?text='+filename, stream=True)
            return File(BytesIO(response.content), name=filename+'.png')
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            return File(BytesIO(response.content), name=filename)
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
    return None

def populate():
    # Clear existing data
    Driver.objects.all().delete()
    Team.objects.all().delete()
    Race.objects.all().delete()
    SeasonStats.objects.all().delete()

    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin')

    teams_data = [
        {'name': 'Mercedes', 'country': 'Germany', 'team_principal': 'Toto Wolff', 'championships': 8},
        {'name': 'Red Bull Racing', 'country': 'Austria', 'team_principal': 'Christian Horner', 'championships': 6},
        {'name': 'Ferrari', 'country': 'Italy', 'team_principal': 'Fred Vasseur', 'championships': 16},
        {'name': 'McLaren', 'country': 'United Kingdom', 'team_principal': 'Andrea Stella', 'championships': 8},
        {'name': 'Aston Martin', 'country': 'United Kingdom', 'team_principal': 'Mike Krack', 'championships': 0},
        {'name': 'Alpine', 'country': 'France', 'team_principal': 'Bruno Famin', 'championships': 2},
    ]

    team_objs = {}
    for t_data in teams_data:
        t = Team.objects.create(
            name=t_data['name'], 
            country=t_data['country'], 
            team_principal=t_data['team_principal'], 
            championships=t_data['championships']
        )
        logo_url = TEAM_LOGOS.get(t_data['name'])
        if logo_url:
            img = get_image(logo_url, f"{t_data['name'].replace(' ', '_')}.png")
            if img:
                t.logo.save(img.name, img)
        team_objs[t.name] = t
        print(f"Created Team: {t.name}")

    drivers_data = [
        {'name': 'Lewis Hamilton', 'number': 44, 'team': 'Mercedes', 'country': 'United Kingdom', 'age': 39, 'championships': 7, 'wins': 103, 'podiums': 197, 'fastest_laps': 65, 'points': 4639.5, 'bio': 'One of the most successful drivers in the history of Formula 1.'},
        {'name': 'Max Verstappen', 'number': 1, 'team': 'Red Bull Racing', 'country': 'Netherlands', 'age': 26, 'championships': 3, 'wins': 54, 'podiums': 98, 'fastest_laps': 30, 'points': 2586.5, 'bio': 'A dominating force in modern Formula 1, known for aggressive racing style.'},
        {'name': 'Charles Leclerc', 'number': 16, 'team': 'Ferrari', 'country': 'Monaco', 'age': 26, 'championships': 0, 'wins': 5, 'podiums': 30, 'fastest_laps': 7, 'points': 1074.0, 'bio': 'A prodigious talent representing the iconic Scuderia Ferrari.'},
        {'name': 'Lando Norris', 'number': 4, 'team': 'McLaren', 'country': 'United Kingdom', 'age': 24, 'championships': 0, 'wins': 0, 'podiums': 13, 'fastest_laps': 6, 'points': 633.0, 'bio': 'A fast and consistent driver leading the youthful charge for McLaren.'},
        {'name': 'Fernando Alonso', 'number': 14, 'team': 'Aston Martin', 'country': 'Spain', 'age': 42, 'championships': 2, 'wins': 32, 'podiums': 106, 'fastest_laps': 24, 'points': 2267.0, 'bio': 'A veteran double World Champion showing incredible longevity.'},
        {'name': 'George Russell', 'number': 63, 'team': 'Mercedes', 'country': 'United Kingdom', 'age': 26, 'championships': 0, 'wins': 1, 'podiums': 11, 'fastest_laps': 6, 'points': 469.0, 'bio': 'The promising British star securing his place among the elites.'},
        {'name': 'Carlos Sainz', 'number': 55, 'team': 'Ferrari', 'country': 'Spain', 'age': 29, 'championships': 0, 'wins': 2, 'podiums': 18, 'fastest_laps': 3, 'points': 982.5, 'bio': 'The smooth operator bringing consistent results for Ferrari.'},
        {'name': 'Sergio Perez', 'number': 11, 'team': 'Red Bull Racing', 'country': 'Mexico', 'age': 34, 'championships': 0, 'wins': 6, 'podiums': 35, 'fastest_laps': 11, 'points': 1486.0, 'bio': 'The Mexican Minister of Defense, an expert at tire management.'},
    ]

    for d_data in drivers_data:
        t_obj = team_objs.get(d_data['team'])
        d = Driver.objects.create(
            name=d_data['name'],
            number=d_data['number'],
            team=t_obj,
            country=d_data['country'],
            age=d_data['age'],
            championships=d_data['championships'],
            wins=d_data['wins'],
            podiums=d_data['podiums'],
            fastest_laps=d_data['fastest_laps'],
            points=d_data['points'],
            bio=d_data['bio']
        )
        img_url = DRIVER_IMAGES.get(d_data['name'])
        if img_url:
            img = get_image(img_url, f"{d_data['name'].replace(' ', '_')}.jpg")
            if img:
                d.image.save(img.name, img)
        print(f"Created Driver: {d.name}")

    print("Successfully populated data")

if __name__ == '__main__':
    populate()
