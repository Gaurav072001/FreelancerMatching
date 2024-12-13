def calculate_score(team, required_skills):
    total_rating = sum(f.rating for f in team)
    team_skills = set(skill for f in team for skill in f.skills)
    skill_coverage = len(required_skills.intersection(team_skills))
    return total_rating + skill_coverage