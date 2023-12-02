from model import db, connect_to_db, Feedback

def create_feedback_message(selected_event_id, coach_id, feedback): 
    
    feedback_message = Feedback(selected_event_id = selected_event_id, 
                coach_id = coach_id,
                feedback = feedback)
    
    return feedback_message