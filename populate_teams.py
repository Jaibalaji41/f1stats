import os
import django
import requests
from io import BytesIO
from django.core.files import File

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'F1StatsHub.settings')
django.setup()

from stats.models import Team

TEAM_DATA = {
    'Ferrari': {'color': '#DC0000', 'logo': 'https://upload.wikimedia.org/wikipedia/en/thumb/c/c0/Scuderia_Ferrari_Logo.svg/1024px-Scuderia_Ferrari_Logo.svg.png'},
    'Mercedes': {'color': '#00D2BE', 'logo': 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/fb/Mercedes_AMG_Petronas_F1_Logo.svg/1024px-Mercedes_AMG_Petronas_F1_Logo.svg.png'},
    'Red Bull Racing': {'color': '#1E41FF', 'logo': 'https://upload.wikimedia.org/wikipedia/en/thumb/8/87/Red_Bull_Racing_logo.svg/1024px-Red_Bull_Racing_logo.svg.png'},
    'McLaren': {'color': '#FF8700', 'logo': 'https://upload.wikimedia.org/wikipedia/en/thumb/6/66/McLaren_Racing_logo.svg/1024px-McLaren_Racing_logo.svg.png'},
    'Williams': {'color': '#005AFF', 'logo': 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f9/Williams_Racing_2020_logo.png/1024px-Williams_Racing_2020_logo.png'},
    'Team Lotus': {'color': '#FFB800', 'logo': 'https://upload.wikimedia.org/wikipedia/en/thumb/3/30/Team_Lotus_logo.svg/1024px-Team_Lotus_logo.svg.png'},
    'Benetton': {'color': '#00A382', 'logo': 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Benetton_Formula_logo.svg/1024px-Benetton_Formula_logo.svg.png'},
    'Brabham': {'color': '#FFFFFF', 'logo': 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Brabham_logo.svg/1024px-Brabham_logo.svg.png'},
    'Tyrrell': {'color': '#004225', 'logo': 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/Tyrrell_Racing_logo.svg/1024px-Tyrrell_Racing_logo.svg.png'},
    'Brawn GP': {'color': '#CEFF00', 'logo': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/Brawn_GP_logo.svg/1024px-Brawn_GP_logo.svg.png'},
    'Aston Martin': {'color': '#006F62', 'logo': 'https://upload.wikimedia.org/wikipedia/en/thumb/e/ef/Aston_Martin_Aramco_Cognizant_F1_Team_logo.svg/1024px-Aston_Martin_Aramco_Cognizant_F1_Team_logo.svg.png'},
    'Alpine': {'color': '#FF87BC', 'logo': 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Alpine_F1_Team_Logo.svg/1024px-Alpine_F1_Team_Logo.svg.png'},
    'Sauber': {'color': '#00E701', 'logo': 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/Sauber_logo.svg/1024px-Sauber_logo.svg.png'},
    'Haas': {'color': '#FFFFFF', 'logo': 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/cd/Haas_F1_Team_logo.svg/1024px-Haas_F1_Team_logo.svg.png'},
}

def get_image(url, filename):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            return File(BytesIO(response.content), name=filename)
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
    return None

def update_teams():
    teams = Team.objects.all()
    for team in teams:
        if team.name in TEAM_DATA:
            data = TEAM_DATA[team.name]
            team.color = data['color']
            img = get_image(data['logo'], f"{team.name.replace(' ', '_')}.png")
            if img:
                team.logo.save(img.name, img)
            team.save()
            print(f"Updated {team.name}")

if __name__ == '__main__':
    update_teams()
