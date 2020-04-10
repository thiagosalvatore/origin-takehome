from datetime import datetime


class RiskProfileService:
    def __init__(self, profile):
        """
        :param profile: The profile sent to the risk API
        """
        self.profile = profile
        self.score = {
            "auto": 0,
            "disability": 0,
            "home": 0,
            "life": 0
        }
        self.risk_profile = {
            "auto": "economic",
            "disability": "economic",
            "home": "economic",
            "life": "economic"
        }

    def calculate_age_score(self):
        age = self.profile["age"]

        if age > 60:
            self.risk_profile["disability"] = "ineligible"
            self.risk_profile["life"] = "ineligible"
        elif age < 30:
            for key in self.score.keys():
                self.score[key] -= 2
        else:
            for key in self.score.keys():
                self.score[key] -= 1
        return self.score

    def calculate_income_score(self):
        if self.profile["income"] > 200000:
            for key in self.score.keys():
                self.score[key] -= 1
        return self.score

    def calculate_house_score(self):
        house = self.profile.get("house")

        if house and house["ownership_status"] == "mortgaged":
            self.score["home"] += 1
            self.score["disability"] += 1

        return self.score

    def calculate_dependent_score(self):
        if self.profile["dependents"] > 0:
            self.score["disability"] += 1
            self.score["life"] += 1
        return self.score

    def calculate_relationship_score(self):
        if self.profile["marital_status"] == "married":
            self.score["life"] += 1
            self.score["disability"] -= 1
        return self.score

    def calculate_vehicle_score(self):
        vehicle = self.profile.get("vehicle")
        current_year = datetime.now().year
        if vehicle:
            diff_year = current_year - vehicle["year"]
            # Vehicles produced in the last 5 years
            if diff_year <= 5:
                self.score["auto"] += 1
        return self.score

    def set_risk_from_score(self):
        for line, score in self.score.items():
            if self.risk_profile[line] != "ineligible":
                if score <= 0:
                    risk = "economic"
                elif score >= 3:
                    risk = "responsible"
                else:
                    risk = "regular"
                self.risk_profile[line] = risk
        return self.risk_profile

    def calculate_risk_profile(self):
        income = self.profile["income"]
        house = self.profile.get("house")
        vehicle = self.profile.get("vehicle")

        if not income and not house and not vehicle:
            self.risk_profile = {
                "auto": "ineligible",
                "disability": "ineligible",
                "home": "ineligible",
                "life": "ineligible"
            }
        else:
            self.calculate_age_score()
            self.calculate_income_score()
            self.calculate_house_score()
            self.calculate_dependent_score()
            self.calculate_relationship_score()
            self.calculate_vehicle_score()

        return self.set_risk_from_score()
