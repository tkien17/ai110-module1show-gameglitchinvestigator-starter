from logic_utils import check_guess

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"


def test_guess_messages_are_correct():
    # Ensure the hint messages match the numeric direction (fixes the high/low bug)
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message

    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message


def test_reset_game_state_resets_session(monkeypatch):
    # Ensure new game resets score/history/status (fixes leftover state bug)
    import streamlit as st
    import app

    st.session_state.clear()
    st.session_state.attempts = 5
    st.session_state.secret = 99
    st.session_state.score = 123
    st.session_state.history = [1, 2, 3]
    st.session_state.status = "lost"

    monkeypatch.setattr(app.random, "randint", lambda a, b: 42)
    app.reset_game_state()

    assert st.session_state.attempts == 0
    assert st.session_state.secret == 42
    assert st.session_state.score == 0
    assert st.session_state.history == []
    assert st.session_state.status == "playing"
