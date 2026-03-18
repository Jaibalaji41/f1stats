from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    championships = models.IntegerField()
    team_principal = models.CharField(max_length=100)
    color = models.CharField(max_length=10, blank=True)
    logo = models.ImageField(upload_to='team_logos/', blank=True, null=True)

    @property
    def static_logo_url(self):
        # Dynamic filename generation: lower case, remove spaces
        slug = self.name.lower().replace(' ', '')
        
        # Handle requested manual overrides/exceptions
        if 'mercedes' in slug: return 'images/mercedes.jpg'
        if 'redbull' in slug: return 'images/redbull.png'
        if 'lotus' in slug: return 'images/lotus.png'
        
        return f"images/{slug}.png"

    @property
    def flag_url(self):
        m = {'Germany': 'de', 'Austria': 'at', 'Italy': 'it', 'United Kingdom': 'gb', 'France': 'fr', 'USA': 'us', 'Switzerland': 'ch'}
        code = m.get(self.country, 'gb')
        return f"https://flagcdn.com/w40/{code}.png"

    def __str__(self):
        return self.name

class Driver(models.Model):
    name = models.CharField(max_length=100)
    number = models.CharField(max_length=10, blank=True, null=True)
    nationality = models.CharField(max_length=100, blank=True, null=True)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='drivers')
    championships = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    podiums = models.IntegerField(default=0)
    fastest_laps = models.IntegerField(default=0)
    career_points = models.FloatField(default=0)
    photo = models.ImageField(upload_to='drivers/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    
    @property
    def flag_url(self):
        m = {
            'British': 'gb', 'Dutch': 'nl', 'Monegasque': 'mc', 'Spanish': 'es', 
            'Mexican': 'mx', 'German': 'de', 'Brazilian': 'br', 'French': 'fr', 
            'Finnish': 'fi', 'Australian': 'au', 'Italian': 'it', 'Canadian': 'ca', 
            'Austrian': 'at', 'Argentine': 'ar', 'Colombian': 'co', 'Japanese': 'jp',
            'New Zealander': 'nz', 'American': 'us', 'South African': 'za', 
            'Swiss': 'ch', 'Swedish': 'se', 'Belgian': 'be', 'Danish': 'dk',
            'Russian': 'ru', 'Polish': 'pl', 'Thai': 'th', 'Chinese': 'cn'
        }
        code = m.get(self.nationality, 'eu')
        return f"https://flagcdn.com/w40/{code}.png"

    def __str__(self):
        return self.name

class SeasonStats(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='season_stats')
    year = models.IntegerField()
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='season_stats')
    races = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    podiums = models.IntegerField(default=0)
    points = models.FloatField(default=0)
    championship_position = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.year} - {self.driver.name}"

class RaceResult(models.Model):
    race_name = models.CharField(max_length=200)
    circuit = models.CharField(max_length=200)
    country = models.CharField(max_length=100)
    race_date = models.DateField()

    def __str__(self):
        return f"{self.race_name} {self.race_date.year}"

class RacePosition(models.Model):
    race = models.ForeignKey(RaceResult, on_delete=models.CASCADE, related_name='positions')
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='race_positions')
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)
    position = models.IntegerField()
    points = models.FloatField(default=0)
    race_time = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"P{self.position} - {self.driver.name} at {self.race.race_name}"
