class Question:
    """Question on a questionnaire."""

    def __init__(self, question, choices=None, allow_text=False):
        """Create question (assume Yes/No for choices."""

        if not choices:
            choices = ["Yes", "No"]

        self.question = question
        self.choices = choices
        self.allow_text = allow_text


    


class Survey:
    """Questionnaire."""

    def __init__(self, title, instructions, questions):
        """Create questionnaire."""

        self.title = title
        self.instructions = instructions
        self.questions = questions

  
    
    


health_survey = Survey(
    "Health Issues Survey",
    "Please fill out a survey about your experience with us.",
    [
        Question("Do you suffer from Asthma and allergies?"),
        Question("Do you suffer from headaches or migraines?"),
        Question("Do you have any type of diabetes?"),
        Question("Do you suffer from joint pain or arthritis?"),
        Question("Do you suffer from heart problems or at risk of a heart attack?"),
    ])

    