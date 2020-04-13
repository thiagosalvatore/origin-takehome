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

    def calculate_base_score(self):
        base_score = sum(self.profile["risk_questions"])
        for key in self.score.keys():
            self.score[key] = base_score
        return self.score

    def calculate_age_score(self):
        """
        If the user is over 60 years old, she is ineligible for disability and life insurance.
        If the user is under 30 years old, deduct 2 risk points from all lines of insurance.
        If she is between 30 and 40 years old, deduct 1.
        """
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
        """
        If the user doesn’t have income, she is ineligible for disability.
        If her income is above $200k, deduct 1 risk point from all lines of insurance.
        """
        income = self.profile["income"]
        if income == 0:
            self.risk_profile["disability"] = "ineligible"
        elif income > 200000:
            for key in self.score.keys():
                self.score[key] -= 1
        return self.score

    def calculate_house_score(self):
        """
        If the user doesn’t have a house, she is ineligible for home insurance.
        If the user's house is mortgaged, add 1 risk point to her home score and
        add 1 risk point to her disability score.
        :return:
        """
        house = self.profile.get("house")

        if not house:
            self.risk_profile["home"] = "ineligible"
        elif house["ownership_status"] == "mortgaged":
            self.score["home"] += 1
            self.score["disability"] += 1

        return self.score

    def calculate_dependent_score(self):
        """
        If the user has dependents, add 1 risk point to both the disability and life scores.
        """
        if self.profile["dependents"] > 0:
            self.score["disability"] += 1
            self.score["life"] += 1
        return self.score

    def calculate_relationship_score(self):
        """
        If the user is married, add 1 risk point to the life score and remove 1 risk point from disability.
        """
        if self.profile["marital_status"] == "married":
            self.score["life"] += 1
            self.score["disability"] -= 1
        return self.score

    def calculate_vehicle_score(self):
        """
        If the user doesn’t have vehicles, she is auto insurance.
        If the user's vehicle was produced in the last 5 years, add 1 risk point to that vehicle’s score.
        """
        vehicle = self.profile.get("vehicle")
        current_year = datetime.now().year
        if vehicle:
            diff_year = current_year - vehicle["year"]
            # Vehicles produced in the last 5 years
            if diff_year <= 5:
                self.score["auto"] += 1
        else:
            self.risk_profile["auto"] = "ineligible"
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
        self.calculate_base_score()
        self.calculate_age_score()
        self.calculate_income_score()
        self.calculate_house_score()
        self.calculate_dependent_score()
        self.calculate_relationship_score()
        self.calculate_vehicle_score()

        return self.set_risk_from_score()
