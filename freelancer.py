class Freelancer:
    def __init__(self, name, skills, hourly_rate, rating, availability, location, domain, projects_completed, soft_skills, reviews):
        self.name = name
        self.skills = skills
        self.hourly_rate = hourly_rate
        self.rating = rating
        self.availability = availability
        self.location = location
        self.domain = domain
        self.projects_completed = projects_completed
        self.soft_skills = soft_skills
        self.reviews = reviews

    def average_review_score(self):
        return sum(self.reviews) / len(self.reviews) if self.reviews else 0

    def __str__(self):
        return (f"{self.name} ({', '.join(self.skills)}, ${self.hourly_rate}/hr, "
                f"Rating: {self.rating}, Location: {self.location}, "
                f"Projects: {self.projects_completed}, Domain: {self.domain})")
