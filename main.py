
from dataclasses import dataclass
from drafter import *
from drafter.components import Component

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


# Sample Initial Data
SAMPLE_EXERCISES = [
    Exercise("Hip Thrusts", 3, "6-8", "Full Gym", "Drive through heels to lift weight."),
    Exercise("Split Squats", 3, "8-10", "Dumbbells", "Lower rear knee toward floor."),
    Exercise("RDLs", 3, "8-10", "Dumbbells", "Hinge at hips keeping back flat.")
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
            Exercise("Bench Press", 4, "5", "Full Gym", "Press bar straight up from chest."),
            Exercise("Push-ups", 3, "12-15", "Bodyweight", "Keep body in a straight plank.")
        ]
    )
]


# 2. Routes

@route
def home(state: State) -> Page:
    return Page(state, [
        Header("Welcome to Workout Finder!"),
        Button("Find a Workout Routine", search_routines),
        Button("View Saved Routines", view_saved_routines)
    ])


@route
def search_routines(state: State) -> Page:
    return Page(state, [
        Header("Search Routines"),
        Text("Select Muscle Group:"),
        SelectBox("muscle", ["Glutes", "Chest", "Legs", "Back"], "Glutes"),
        Text("Select Equipment:"),
        SelectBox("equipment", ["Full Gym", "Dumbbells", "Bodyweight"], "Full Gym"),
        Button("Search", show_results),
        Button("Home", home)
    ])


@route
def show_results(state: State, muscle: str = "", equipment: str = "") -> Page:
    state.selected_muscle = muscle
    state.selected_equipment = equipment

    results = []
    for routine in state.database:
        if routine.muscle_group == state.selected_muscle:
            results.append(routine)

    state.search_results = results

    content: list[Component] = [Header("Matching Routines")]

    if len(state.search_results) == 0:
        content.append(Text("No matching routines found."))
    else:
        for index, routine in enumerate(state.search_results):
            content.append(Text(f"#{index + 1}: {routine.name}"))
            content.append(
                Button("View Routine", view_routine,
                       arguments={"routine_index": index})
            )

    content.append(Button("Search Again", search_routines))
    content.append(Button("Clear Search", clear_search))

    return Page(state, content)


@route
def view_routine(state: State, routine_index: int) -> Page:
    routine = state.search_results[routine_index]

    content: list[Component] = [
        Header("Routine Details"),
        Text(routine.name),
        Text(routine.description),
        Text("Exercises:")
    ]

    for ex in routine.exercises:
        content.append(Text(f"{ex.name} - {ex.sets} sets x {ex.reps} reps"))

    content.append(
        Button("Save Routine", save_routine,
               arguments={"routine_index": routine_index})
    )
    content.append(Button("Back to Results", show_results))

    return Page(state, content)


@route
def save_routine(state: State, routine_index: int) -> Page:
    routine = state.search_results[routine_index]
    state.saved_routines.append(routine)
    return view_saved_routines(state)


@route
def view_saved_routines(state: State) -> Page:
    content: list[Component] = [Header("Saved Routines")]

    if len(state.saved_routines) == 0:
        content.append(Text("You have no saved routines."))
    else:
        for index, routine in enumerate(state.saved_routines):
            content.append(Text(routine.name))
            content.append(
                Button("Remove Routine", remove_routine,
                       arguments={"routine_index": index})
            )

    content.append(Button("Home", home))

    return Page(state, content)


@route
def remove_routine(state: State, routine_index: int) -> Page:
    state.saved_routines.pop(routine_index)
    return view_saved_routines(state)


@route
def clear_search(state: State) -> Page:
    state.search_results = []
    return search_routines(state)


# 3. Launch
initial_state = State(
    database=SAMPLE_ROUTINES,
    search_results=[],
    saved_routines=[],
    selected_muscle="",
    selected_equipment=""
)

start_server(initial_state)

