from src.utils.switchers import meeting_switcher, school_switcher


def collect_week_data(frame):
    data = []
    week = frame.weeks[0][0]
    for assignation in frame.assignations:
        key = assignation["key"]
        if assignation["school"]:
            if frame.widgets["checkbox_" + key].get():
                assignment_type = school_switcher(frame.widgets["option_type_" + key].get())
                titular = frame.widgets["option0_" + key].get()
                companion = frame.widgets["option1_" + key].get()
                if companion:
                    data.append([assignment_type, titular, week, companion])
                else:
                    data.append([assignment_type, titular, week])
        else:
            assignment_type = meeting_switcher(frame.widgets["checkbox_" + key].cget("text"))
            titular = frame.widgets["option_" + key].get()
            data.append([assignment_type, titular, week])
    return data


def write_week_log(frame):
    frame.write_to_file("-------------------------------")
    frame.write_to_file(str(frame.label_week.cget("text")))
    for assignation in frame.assignations:
        key = assignation["key"]
        if assignation["school"]:
            if frame.widgets["checkbox_" + key].get():
                assignment = frame.widgets["option_type_" + key].get()
                titular = frame.widgets["option0_" + key].get()
                companion = frame.widgets["option1_" + key].get()
                frame.write_to_file(assignment + ": " + titular + " - " + companion)
        else:
            assignment = frame.widgets["checkbox_" + key].cget("text")
            titular = frame.widgets["option_" + key].get()
            frame.write_to_file(assignment + ": " + titular)
