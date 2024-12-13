from flask import Flask, render_template, request, redirect, jsonify
import sqlite3
from freelancer import Freelancer
from team_formation import knapsack_with_criteria
from compatibility_score import calculate_score

app = Flask(__name__)

def add_freelancer_to_db(freelancer):
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO freelancers(name, skills, hourly_rate, rating, availability,
                   location_lat, location_lon, domain, projects_completed,
                   soft_skills, reviews)
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,(freelancer.name,",".join(freelancer.skills), freelancer.hourly_rate, freelancer.rating,
         freelancer.availability, freelancer.location["lat"], freelancer.location["lon"],
         freelancer.domain, freelancer.projects_completed, ",".join(freelancer.soft_skills),
         ",".join(map(str, freelancer.reviews))))
    conn.commit()
    conn.close()

def fetch_freelancers_from_db():
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    cursor.execute("SELECT * From freelancers")
    rows = cursor.fetchall()
    conn.close()

    freelancers = []
    for row in rows:
        freelancers.append(Freelancer(
            name=row[1],
            skills=row[2].split(","),
            hourly_rate=row[3],
            rating=row[4],
            availability=row[5],
            location={"lat": row[6], "lon" : row[7]},
            domain=row[8],
            projects_completed=row[9],
            soft_skills=row[10].split(","),
            reviews=list(map(int,row[11].split(",")))
        ))
    return freelancers

#Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        data = request.form
        freelancer = Freelancer(
            name=data["name"],
            skills=data["skills"].split(","),
            hourly_rate=float(data["hourly_rate"]),
            rating=float(data["rating"]),
            availability=int(data["availability"]),
            location={"lat": float(data["location_lat"]),"lon": float(data["location_lon"])},
            domain=data["domain"],
            projects_completed=int(data["projects_completed"]),
            soft_skills=data["soft_skills"].split(","),
            reviews=[int(r) for r in data["reviews"].split(",")]
        )
        add_freelancer_to_db(freelancer)
        return redirect("/")
    return render_template("register.html")

@app.route("/hire", methods=["GET","POST"])
def hire():
    if request.method == "POST":
        data = request.json
        required_skills = set(data.get("skills", []))
        budget = data.get("budget", 0)
        preferred_location = data.get("location",None)

        if preferred_location:
            preferred_location = (preferred_location["lat"], preferred_location["lon"])
        
        freelancers = fetch_freelancers_from_db()
        team = knapsack_with_criteria(freelancers, budget, required_skills,preferred_location)
        score=calculate_score(team,required_skills)

        team_data = [{"name": f.name, "skills":f.skills, "hourly_rate": f.hourly_rate,
                      "rating": f.rating, "location": f.location, "domain": f.domain}
                      for f in team]
        return jsonify({"team": team_data, "score": score})
    return render_template("hire.html")

if __name__ == "__main__":
    app.run(debug=True)
