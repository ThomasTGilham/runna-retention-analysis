# Analysis of Runner Personas & Retention Drivers  
*A proactive analysis project for the Data Analyst role at Runna.*

## Project Goal  
To understand the distinct behaviors of different runner archetypes and identify key early indicators of long-term user retention.

---

## Methodology  
A synthetic dataset of 200 users over 16 weeks was programmatically generated to model five distinct runner personas. The process and code can be found in `generate_data.py`. My own Strava activity was included as a real-world control group.

---

## Key Insight: A Clear Decision Boundary  
Initial modeling with logistic regression revealed **complete separation** in the data, meaning the behavioral differences between retained and lapsed users were perfectly predictable.

To visualize this clear rule, a **Decision Tree classifier** was trained. The result shows that a user's **maximum run distance in their first month** is the single most powerful predictor of long-term engagement.

![alt text](https://github.com/[username]/[reponame]/blob/[branch]/image.jpg?raw=true)

---

## Final Recommendation for Runna  
The analysis indicates that users who complete a *"long-ish"* run (e.g., **>6.5 km**) early in their journey are overwhelmingly likely to become long-term, retained users.

**Recommendation:**  
Design and test an onboarding journey or a **"First Big Run" challenge** aimed at guiding new users to complete their first **>6.5 km run** within their first month on the platform. This could be a powerful lever for improving overall user retention.

---

## Interactive Dashboard  
An interactive version of these findings can be explored on Tableau Public:  
[Link to your dashboard]

![alt text](https://github.com/[username]/[reponame]/blob/[branch]/image.jpg?raw=true)

