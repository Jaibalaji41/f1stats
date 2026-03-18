from django.shortcuts import render, get_object_or_404
from .models import Team, Driver, RaceResult, SeasonStats, RacePosition

def teams_list(request):
    teams = Team.objects.all().order_by('-championships', 'name')
    return render(request, 'stats/home.html', {'teams': teams})

def team_detail(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    drivers = team.drivers.all().order_by('-championships', '-wins')
    return render(request, 'stats/team_detail.html', {'team': team, 'drivers': drivers})

def drivers_list(request):
    search_query = request.GET.get('search', '')
    team_filter = request.GET.get('team', '')
    sort_by = request.GET.get('sort', 'wins')
    
    drivers = Driver.objects.all()
    
    if search_query:
        drivers = drivers.filter(name__icontains=search_query)
    
    if team_filter:
        drivers = drivers.filter(team__id=team_filter)
        
    if sort_by == 'points':
        drivers = drivers.order_by('-career_points', '-wins')
    else:
        drivers = drivers.order_by('-wins', '-career_points')
        
    teams = Team.objects.all().order_by('name')
    
    return render(request, 'stats/drivers.html', {
        'drivers': drivers,
        'teams': teams,
        'search_query': search_query,
        'team_filter': team_filter,
        'sort_by': sort_by
    })

def driver_detail(request, driver_id):
    driver = get_object_or_404(Driver, id=driver_id)
    season_stats = driver.season_stats.all().order_by('year')
    return render(request, 'stats/driver_detail.html', {
        'driver': driver,
        'season_stats': season_stats
    })

def driver_compare(request):
    d1_id = request.GET.get('driver1')
    d2_id = request.GET.get('driver2')
    
    driver1 = None
    driver2 = None
    
    if d1_id and d2_id:
        driver1 = Driver.objects.filter(id=d1_id).first()
        driver2 = Driver.objects.filter(id=d2_id).first()
        
    all_drivers = Driver.objects.all().order_by('name')
        
    return render(request, 'stats/compare.html', {
        'driver1': driver1,
        'driver2': driver2,
        'all_drivers': all_drivers,
        'd1_id': int(d1_id) if d1_id else '',
        'd2_id': int(d2_id) if d2_id else ''
    })

def races_list(request):
    races = RaceResult.objects.filter(race_date__year__gte=2023).order_by('-race_date')
    return render(request, 'stats/races.html', {'races': races})
