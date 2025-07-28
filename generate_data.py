
# Runner Personas
# 1. Consistent Trainer
# A dedicated runner who maintains a steady and frequent training schedule week after week. They are the ideal, highly-retained user, gradually improving their fitness over time.
# 
# 2. Weekend Warrior
# This runner squeezes most of their activity into the weekend, often completing one long run. They are consistent in their weekly habit but less frequent than a daily trainer.
# 
# 3. Lapsed Newcomer
# A new user who starts with high enthusiasm and frequency but whose activity drops off completely after 3-4 weeks. This persona represents a key churn risk for the business.
# 
# 4. Event-Driven Racer
# A goal-oriented runner whose training is structured around a specific race. Their activity shows a clear build-up, a pre-race taper, and a significant change in behavior after the event, posing a re-engagement challenge.
# 
# 5. Boom-and-Bust Runner
# An enthusiastic but potentially inexperienced runner who increases their training load too quickly, leading to a predictable cycle of overtraining, a forced "injury" layoff, and a tentative return.


import pandas as pd
import numpy as np
import datetime



# --- Parameters from your EDA of your own Strava activity data ---
BASE_DIST_MEAN = 8.47
BASE_DIST_STD = 5.51
BASE_PACE_MEAN = 4.77 # Approx 4:45 min/km - This is a strong baseline
BASE_PACE_STD = 0.60

# The corrected function definition
def modify_event_racer_behavior(day, distance, is_weekend, race_day=90, **kwargs):
    """Modifies run distance based on a training plan for a race on race_day."""
    days_until_race = race_day - day

    if days_until_race < -7:  # More than a week after the race
        return distance * 0.4  # Settle into light maintenance running
    elif days_until_race <= 0: # Recovery week (includes race day)
        return None  # No running
    elif days_until_race == 0: # Race Day!
        return 42.2  # Marathon distance
    elif days_until_race <= 14: # 2-week taper
        return distance * 0.6
    elif days_until_race <= 84: # 12-week peak training block
        # Simulate a weekend long run by adding significant distance
        if is_weekend:
            return distance + 10
        else:
            return distance
    else: # Base building
        return distance

# --- The Main Personas Dictionary ---
personas = {
    'Consistent Trainer': {
        'run_prob_weekday': 0.45, # Represents ~3 runs on weekdays
        'run_prob_weekend': 0.6, # Represents ~1 run on the weekend
        'dist_mean': BASE_DIST_MEAN,
        'dist_std': BASE_DIST_STD,
        'pace_mean': BASE_PACE_MEAN,
        'pace_std': BASE_PACE_STD,
        # Gradual fitness improvement over 120 days
        'behavior_modifier': lambda **kwargs: kwargs['pace'] - (kwargs['day'] * 0.0015)
    },
    'Weekend Warrior': {
        'run_prob_weekday': 0.1, # One short run during the week is possible
        'run_prob_weekend': 0.8, # Very likely to do a weekend run
        'dist_mean': BASE_DIST_MEAN + 4, # Avg distance is ~12.5km (long run focus)
        'dist_std': BASE_DIST_STD + 1.5, # More variance in long run distances
        'pace_mean': BASE_PACE_MEAN + 0.2, # Slightly slower pace for longer runs (~5:00 min/km)
        'pace_std': BASE_PACE_STD,
        'behavior_modifier': lambda **kwargs: kwargs['pace'] # Stable behavior
    },
    'Lapsed Newcomer': {
        'run_prob_weekday': 0.6, # Starts with high frequency
        'run_prob_weekend': 0.5,
        'dist_mean': BASE_DIST_MEAN - 4, # Avg distance is ~4.5km (beginner distance)
        'dist_std': BASE_DIST_STD * 0.5, # Less variance in distances
        'pace_mean': BASE_PACE_MEAN + 1.2, # Significantly slower pace (~6:00 min/km)
        'pace_std': BASE_PACE_STD * 0.8, # Less pace variance
        # Stops running completely after 28 days
        'behavior_modifier': lambda **kwargs: kwargs['pace'] if kwargs['day'] < 28 else None
    },
    'Event-Driven Racer': {
        'run_prob_weekday': 0.5, # Structured training implies ~3-4 runs/week
        'run_prob_weekend': 0.7,
        'dist_mean': BASE_DIST_MEAN,
        'dist_std': BASE_DIST_STD,
        'pace_mean': BASE_PACE_MEAN - 0.25, # Noticeably faster than base (~4:30 min/km)
        'pace_std': BASE_PACE_STD * 0.9, # More consistent pacing
        # The complex logic is handled by the dedicated function
        'behavior_modifier': modify_event_racer_behavior
    },
    'Boom-and-Bust': {
        'run_prob_weekday': 0.7, # High frequency suggests overtraining
        'run_prob_weekend': 0.8,
        'dist_mean': BASE_DIST_MEAN - 2, # Moderate distance ~6.5km
        'dist_std': BASE_DIST_STD * 0.7,
        'pace_mean': BASE_PACE_MEAN,
        'pace_std': BASE_PACE_STD,
        # This persona's logic is too complex for a lambda.
        # It must be handled by a "state machine" in your main generation loop.
        'behavior_modifier': lambda **kwargs: kwargs['distance']
    }
}

# --- Simulation Parameters ---
NUM_USERS = 250
START_DATE = datetime.date(2025, 1, 1)
SIMULATION_DAYS = 120 # Approx 16 weeks

# --- Main Generation Loop ---
all_activities = []
user_personas = {}

print("Generating user data... This may take a moment.")

for user_id in range(1, NUM_USERS + 1):
    # --- 1. Initialize User-Specific State ---
    persona_name = np.random.choice(list(personas.keys()))
    print(f"Assigning User {user_id} as: {persona_name}")
    user_personas[user_id] = persona_name
    persona_params = personas[persona_name]
    
    # Initialize state variables for all users (most will go unused)
    user_start_date = START_DATE + datetime.timedelta(days=np.random.randint(0, 30))
    user_race_day = np.random.randint(80, 110) # Assign a race day between day 80-110
    
    # State for the 'Boom-and-Bust' persona
    user_state = 'training'  # States: 'training', 'injured', 'recovering'
    injury_cooldown = 0
    weekly_mileage_log = {week: 0 for week in range(53)}

    # --- Daily Simulation Loop for this User ---
    for day in range(SIMULATION_DAYS):
        current_date = user_start_date + datetime.timedelta(days=day)
        is_weekend = current_date.weekday() >= 5
        current_week = current_date.isocalendar().week

        # --- 2. State Machine Logic (Applied before run generation) ---
        if persona_name == 'Boom-and-Bust':
            # If injured, decrement cooldown and skip to the next day
            if user_state == 'injured':
                injury_cooldown -= 1
                if injury_cooldown <= 0:
                    user_state = 'recovering' # Recovery starts after layoff
                continue

            # At the end of a week, check for overtraining
            if current_date.weekday() == 6: # Sunday
                w_minus_1 = weekly_mileage_log.get(current_week - 1, 0)
                w_minus_2 = weekly_mileage_log.get(current_week - 2, 0)
                if w_minus_1 > w_minus_2 * 1.5 and w_minus_2 > 0: # Overtraining check
                    user_state = 'injured'
                    injury_cooldown = 21 # 3-week layoff
                    continue

        # --- 3. Run Probability Check ---
        run_prob = persona_params['run_prob_weekend'] if is_weekend else persona_params['run_prob_weekday']
        if np.random.rand() < run_prob:
            
            # --- 4. Generate Base Run Stats ---
            distance = np.random.normal(loc=persona_params['dist_mean'], scale=persona_params['dist_std'])
            pace = np.random.normal(loc=persona_params['pace_mean'], scale=persona_params['pace_std'])

            # --- 5. Apply Persona-Specific Behavior Modifiers ---
            kwargs = {'day': day, 'distance': distance, 'pace': pace, 'is_weekend': is_weekend, 'race_day': user_race_day}
            
            # The 'behavior_modifier' for most personas modifies pace. For the racer, it modifies distance.
            if persona_name == 'Event-Driven Racer':
                distance = persona_params['behavior_modifier'](**kwargs)
                modified_pace = pace # Pace is not modified for this persona
            else:
                 modified_pace = persona_params['behavior_modifier'](**kwargs)

            # For the 'Boom-and-Bust' runner in recovery, penalize their distance
            if persona_name == 'Boom-and-Bust' and user_state == 'recovering':
                 distance *= 0.5

            # --- 6. Finalize and Append Activity ---
            if distance is None or modified_pace is None:
                continue

            distance = max(1, distance)
            pace = max(3, modified_pace)
            
            moving_time_seconds = (pace * 60) * distance
            
            all_activities.append({
                'activity_id': f'act_{user_id}_{day}',
                'user_id': user_id,
                'persona': persona_name,
                'activity_date': current_date,
                'distance_km': round(distance, 2),
                'pace_min_km': round(pace, 2),
                'moving_time_sec': int(moving_time_seconds)
            })
            
            # --- 7. Update State (after a successful run) ---
            if persona_name == 'Boom-and-Bust':
                weekly_mileage_log[current_week] += distance

print(f"Generated {len(all_activities)} activities for {NUM_USERS} users.")


# Quick test for persona assignment
import numpy as np

# Make sure your 'personas' dictionary is defined correctly before this
test_assignments = [np.random.choice(list(personas.keys())) for _ in range(200)]
from collections import Counter
print(Counter(test_assignments))


# --- Create and Save the Final DataFrame ---
df_synthetic = pd.DataFrame(all_activities)

# Save to CSV
output_path = 'synthetic_runna_data.csv'
df_synthetic.to_csv(output_path, index=False)

print(f"Synthetic data successfully saved to {output_path}")




