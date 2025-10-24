# 🏋️‍♂️ WorkoutTracker

**WorkoutTracker** is a fitness analytics dashboard built with **Python** and **Streamlit**.  
It helps you visualize your training progress, analyze trends, and stay motivated by tracking your workout history.

---

## 🚀 Live Demo
🔗 [Try the app on Streamlit Cloud](https://workout-analyser.streamlit.app)

---

## 📸 Preview
![App Screenshot](images/workout_analyser_demo.png)

---

## 🚀 Features

- 📅 **Workout calendar** – Interactive heatmap of training activity  
- 📈 **Trends and charts** – Track volume, duration and intensity over time
- 🏆 **Top exercises** – Automatically identifies your most frequent lifts  
- 🔥 **Streak tracker** – Calculates your best week streak (e.g., 4+ workouts/week)  
- 🎯 **Goals & achievements** – Set goals and monitor your progress  
- 💪 **Motivational dashboard** – Keep your consistency visible and rewarding  

---

## 🧠 Tech Stack

- **Frontend / UI:** [Streamlit](https://streamlit.io/) + [streamlit-option-menu](https://github.com/victoryhb/streamlit-option-menu)
- **Data handling:** Pandas, NumPy
- **Visualization:** Matplotlib, Plotly
- **File input:** CSV upload (export from fitness tracker apps or spreadsheets)
- **Streamlit Cloud:** Deployed on Streamlit Community Cloud

---

## 🗂️ Input Data Format

The app expects a CSV file with the following structure. Each row represents a single set of an exercise.

| title | start_time | end_time | description | exercise_title | superset_id | exercise_notes | set_index | set_type | weight_kg | reps |
|-------|------------|---------|-------------|----------------|-------------|----------------|-----------|----------|-----------|------|
| Push  | 17 Oct 2025, 20:14 | 17 Oct 2025, 21:39 |  | Bench Press (Barbell) |  |  | 3 | warmup  | 80  | 4 |
| Push  | 17 Oct 2025, 20:14 | 17 Oct 2025, 21:39 |  | Bench Press (Barbell) |  |  | 4 | normal  | 100 | 9 |
| Push  | 17 Oct 2025, 20:14 | 17 Oct 2025, 21:39 |  | Bench Press (Barbell) |  |  | 5 | normal  | 100 | 9 |
| Push  | 17 Oct 2025, 20:14 | 17 Oct 2025, 21:39 |  | Bench Press (Barbell) |  |  | 6 | normal  | 100 | 8 |
| Push  | 17 Oct 2025, 20:14 | 17 Oct 2025, 21:39 |  | Bench Press (Barbell) |  |  | 7 | normal  | 100 | 8 |
| Push  | 17 Oct 2025, 20:14 | 17 Oct 2025, 21:39 |  | Triceps Dip (Weighted) |  |  | 0 | warmup  |     | 6 |
| Push  | 17 Oct 2025, 20:14 | 17 Oct 2025, 21:39 |  | Triceps Dip (Weighted) |  |  | 1 | warmup  | 15  | 3 |
| Push  | 17 Oct 2025, 20:14 | 17 Oct 2025, 21:39 |  | Triceps Dip (Weighted) |  |  | 2 | normal  | 32.5| 9 |
| Push  | 17 Oct 2025, 20:14 | 17 Oct 2025, 21:39 |  | Triceps Dip (Weighted) |  |  | 3 | normal  | 32.5| 7 |

### 📝 Field Descriptions
- **title** – name of workout routine (Push/Pull/Arms etc.)
- **start_time** – start datetime of the workout
- **end_time** – end datetime of the workout
- **description** – optional note about the workout
- **exercise_title** – name of the exercise
- **superset_id** – if the exercise is part of a superset, the ID goes here
- **exercise_notes** – any additional notes about the exercise
- **set_index** – index of the set in the exercise
- **set_type** – type of set (`warmup`, `normal`, `drop`, `failure`, etc.)  
- **weight_kg** – weight used in kilograms (empty if bodyweight)  
- **reps** – number of repetitions in the set  

### 💡 Tips
- **Required columns:** `exercise_title`, `set_type`, `reps`, `weight_kg`
- **Optional columns:** `description`, `exercise_notes`  
- If a required column is missing, the app will show an error message.

### 📥 Example CSV
Try the app with the following example:
📥 [Download example CSV](example_workout.csv)


If your data comes from sensors (e.g. smartwatch), make sure to rename or format columns to match the above before upload.