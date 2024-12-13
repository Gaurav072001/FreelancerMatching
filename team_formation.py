from geopy.distance import geodesic  # Install this with `pip install geopy`

def knapsack_with_criteria(freelancers, budget, required_skills, preferred_location=None):
    def calculate_location_score(freelancer):
        if not preferred_location:
            return 1  # Neutral score
        freelancer_location = (freelancer.location['lat'], freelancer.location['lon'])
        distance = geodesic(preferred_location, freelancer_location).km
        return max(0, 1 - distance / 100)  # Closer freelancers get a higher score

    n = len(freelancers)
    dp = [[0] * (int(budget) + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for b in range(int(budget) + 1):
            freelancer = freelancers[i - 1]
            location_score = calculate_location_score(freelancer)
            skill_score = len(required_skills.intersection(freelancer.skills))
            total_score = freelancer.rating * 0.5 + skill_score * 0.3 + location_score * 0.2

            if freelancer.hourly_rate <= b:
                dp[i][b] = max(dp[i - 1][b], dp[i - 1][b - int(freelancer.hourly_rate)] + total_score)
            else:
                dp[i][b] = dp[i - 1][b]

    selected = []
    b = int(budget)
    for i in range(n, 0, -1):
        if dp[i][b] != dp[i - 1][b]:
            selected.append(freelancers[i - 1])
            b -= int(freelancers[i - 1].hourly_rate)

    return selected
