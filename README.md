# Analysis of Runner Personas & Retention Drivers  
*A proactive analysis project for the Data Analyst role at Runna.*

## Project Goal  
To understand the distinct behaviors of different runner archetypes and identify key early indicators of long-term user retention.

---

## Methodology  
A synthetic dataset of 200 users over 16 weeks was programmatically generated to model five distinct runner personas:

1. ***Consistent Trainer***: A dedicated runner who maintains a steady and frequent training schedule week after week. They are the ideal, highly-retained user, gradually improving their fitness over time.
   
2. ***Weekend Warrior***: This runner squeezes most of their activity into the weekend, often completing one long run. They are consistent in their weekly habit but less frequent than a daily trainer.

3. ***Lapsed Newcomer***: A new user who starts with high enthusiasm and frequency but whose activity drops off completely after 3-4 weeks. This persona represents a key churn risk for the business.

4. ***Event-Driven Racer***: A goal-oriented runner whose training is structured around a specific race. Their activity shows a clear build-up, a pre-race taper, and a significant change in behavior after the event, posing a re-engagement challenge.

5. ***Boom-and-Bust Runner***: An enthusiastic but potentially inexperienced runner who increases their training load too quickly, leading to a predictable cycle of overtraining, a forced "injury" layoff, and a tentative return.

The process and code can be found in `generate_data.py`. My own Strava activity was included as a real-world control group.

---

## Key Insight: A Clear Decision Boundary  
Initial modeling with logistic regression revealed **complete separation** in the data, meaning the behavioral differences between retained and lapsed users were perfectly predictable.

To visualize this clear rule, a **Decision Tree classifier** was trained. The result shows that a user's **average runring pace in their first month** is the single most powerful predictor of long-term engagement.

![alt text](https://github.com/ThomasTGilham/runna-retention-analysis/blob/main/decision_tree.png?raw=true)

---

## Final Recommendation for Runna  
This finding suggests that users who are either already fit or who quickly see improvements in their speed in their first four weeks (e.g., **<5.34 min/km pace**) early in their journey are overwhelmingly likely to become long-term, retained users.

**Recommendation:**  
**I recommend that Runna design and test an onboarding plan focused on "First Pace Milestone."** This could involve introducing new users to structured workouts like **tempo runs** or **interval training** early in their journey, helping them tangibly improve their pace and build confidence, which this analysis shows is a critical factor for long-term engagement.

---

## Interactive Dashboard  
An interactive version of these findings can be explored on Tableau Public:  
[Link to your dashboard]

![alt text](https://github.com/[username]/[reponame]/blob/[branch]/image.jpg?raw=true)

