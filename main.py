
from dataclasses import dataclass
from typing import Any
from drafter import *

# Website information
set_website_title("Workout Finder")
set_site_information(
    author="Kamdyn Shockley",
    description="Search for muscle targeted workout routines!",
    sources="Thanks to the Drafter docs and my study group.",
    planning="plan.pdf",
    links=["https://github.com/kshock-08/your-repository"]
)
hide_debug_information()
set_website_framed(False)


# 1. Dataclasses

@dataclass
class Exercise:
    name: str
    sets: int
    reps: str
    equipment: str
    instructions: str


@dataclass
class WorkoutRoutine:
    name: str
    muscle_group: str
    fitness_goal: str
    description: str
    exercises: list[Exercise]


@dataclass
class State:
    database: list[WorkoutRoutine]
    search_results: list[WorkoutRoutine]
    saved_routines: list[WorkoutRoutine]
    selected_muscle: str
    selected_equipment: str


# 2. Sample Initial Data

SAMPLE_EXERCISES = [
    Exercise(
        "Hip Thrusts", 3, "6-8", "Full Gym",
        "Drive through heels to lift weight."
    ),
    Exercise(
        "Split Squats", 3, "8-10", "Dumbbells",
        "Lower rear knee toward floor."
    ),
    Exercise(
        "RDLs", 3, "8-10", "Dumbbells",
        "Hinge at hips keeping back flat."
    )
]

SAMPLE_ROUTINES = [
    WorkoutRoutine(
        "Glute Growth Routine",
        "Glutes",
        "Muscle Gain",
        "Focuses on lower body growth.",
        SAMPLE_EXERCISES
    ),
    WorkoutRoutine(
        "Upper Body Blast",
        "Chest",
        "Strength",
        "Builds chest and arm power.",
        [
            Exercise(
                "Bench Press", 4, "5", "Full Gym",
                "Press bar straight up from chest."
            ),
            Exercise(
                "Push-ups", 3, "12-15", "Bodyweight",
                "Keep body in a straight plank."
            )
        ]
    )
]


# 3. Routes


# Main Homepage
@route
def index(state: State) -> Page:
    return Page(state, [
        Header("Welcome to Workout Finder!"),
        Text("Find workout routines based on your fitness goals."),
        Button("Find a Workout Routine", "search_routines"),
        Button("View Saved Routines", "view_saved_routines")
    ])


# Search Page
@route
def search_routines(state: State) -> Page:
    return Page(state, [
        Header("Search Routines"),

        Text("Select Muscle Group:"),
        SelectBox(
            "muscle",
            ["Glutes", "Chest", "Legs", "Back"],
            state.selected_muscle
        ),

        Text("Select Equipment:"),
        SelectBox(
            "equipment",
            ["Full Gym", "Dumbbells", "Bodyweight"],
            state.selected_equipment
        ),

        Button("Search", "show_results"),
        Button("Home", "index")
    ])


# Display Matching Results
@route
def show_results(
    state: State,
    muscle: str = "",
    equipment: str = ""
) -> Page:

    if muscle == "":
        muscle = state.selected_muscle

    if equipment == "":
        equipment = state.selected_equipment

    state.selected_muscle = muscle
    state.selected_equipment = equipment

    results: list[WorkoutRoutine] = []

    for routine in state.database:
        if routine.muscle_group == muscle:
            for exercise in routine.exercises:
                if exercise.equipment == equipment:
                    results.append(routine)
                    break

    state.search_results = results

    content: list[Any] = [
        Header("Matching Routines")
    ]

    if len(state.search_results) == 0:
        content.append(Text("No matching routines found."))
    else:
        for index, routine in enumerate(state.search_results):
            content.append(Text(f"#{index + 1}: {routine.name}"))
            content.append(Text(routine.description))
            content.append(
                Button(
                    "View Routine",
                    "view_routine",
                    {"routine_index": index}
                )
            )

    content.append(Button("Search Again", "search_routines"))
    content.append(Button("Clear Search", "clear_search"))
    content.append(Button("Home", "index"))

    return Page(state, content)


# View Individual Routine
@route
def view_routine(state: State, routine_index: int) -> Page:

    routine = state.search_results[routine_index]

    content: list[Any] = [
        Header("Routine Details"),
        Text(routine.name),
        Text(routine.description),
        Text("Fitness Goal: " + routine.fitness_goal),
        Text("Muscle Group: " + routine.muscle_group),
        Text("Exercises:")
    ]

    for exercise in routine.exercises:
        content.append(Text("--------------------"))
        content.append(Text("Exercise: " + exercise.name))
        content.append(
            Text(f"Sets: {exercise.sets} x Reps: {exercise.reps}")
        )
        content.append(Text("Equipment: " + exercise.equipment))
        content.append(Text("Instructions: " + exercise.instructions))

    content.append(
        Button(
            "Save Routine",
            "save_routine",
            {"routine_index": routine_index}
        )
    )

    content.append(Button("Back to Results", "show_results"))
    content.append(Button("Home", "index"))

    return Page(state, content)


# Save a Routine
@route
def save_routine(state: State, routine_index: int) -> Page:

    routine = state.search_results[routine_index]

    if routine not in state.saved_routines:
        state.saved_routines.append(routine)

    return view_saved_routines(state)


# View Saved Routines
@route
def view_saved_routines(state: State) -> Page:

    content: list[Any] = [
        Header("Saved Routines")
    ]

    if len(state.saved_routines) == 0:
        content.append(Text("You have no saved routines."))
    else:
        for index, routine in enumerate(state.saved_routines):
            content.append(Text(routine.name))
            content.append(Text(routine.description))

            content.append(
                Button(
                    "Remove Routine",
                    "remove_routine",
                    {"routine_index": index}
                )
            )

    content.append(Button("Home", "index"))

    return Page(state, content)


# Remove a Saved Routine
@route
def remove_routine(state: State, routine_index: int) -> Page:

    state.saved_routines.pop(routine_index)

    return view_saved_routines(state)


# Clear Search
@route
def clear_search(state: State) -> Page:

    state.search_results = []
    state.selected_muscle = "Glutes"
    state.selected_equipment = "Full Gym"

    return search_routines(state)


# 4. Launch Application

initial_state = State(
    database=SAMPLE_ROUTINES,
    search_results=[],
    saved_routines=[],
    selected_muscle="Glutes",
    selected_equipment="Full Gym"
)

start_server(initial_state)




