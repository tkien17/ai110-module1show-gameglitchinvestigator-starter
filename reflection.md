# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

### Bug 1: Hints Are Inverted (Logic Bug)
**Expected:** When my guess is too low, the game should say "Go HIGHER."
When my guess is too high, it should say "Go LOWER."

**What Actually Happened:** The hints were backwards. I guessed 50 when the
secret was 92, but the game said "Go LOWER." I then guessed 95 and it said
"Go HIGHER." The hint logic in `check_guess()` has the comparisons flipped:
`if guess > secret: return "Too High", "📈 Go HIGHER!"` — "Too High" should
map to "Go LOWER", not "Go HIGHER."


### Bug 2: New Game Does Not Reset Score or History 
**Expected:** Clicking "New Game" should reset everything (score back to 0),
history cleared, attempts back to 0.

**What Actually Happened:** Only the secret number and attempts were reset.
The score kept accumulating across games and the history list kept growing,
carrying over guesses from the previous round. This is because the New Game
handler only resets `attempts` and `secret`, not `score`, `history`,
or `status`.


### Bug 3: Attempts Counter Starts at 1, Not 0 (Initialization Bug)
**Expected:** At the start of the game, attempts used should be 0,
and "Attempts left" should show the full limit (e.g., 8 for Normal).

**What Actually Happened:** `st.session_state.attempts` is initialized to `1`
instead of `0`, so the player immediately loses one attempt before making
any guess. The "Attempts left" display is off by one from the very beginning.


### Bug 4: Secret Converted to String on Even Attempts (Type Bug)
**Expected:** Every guess should be compared consistently against the integer
secret number.

**What Actually Happened:** On even-numbered attempts, the code converts the
secret to a string (`secret = str(st.session_state.secret)`) before calling
`check_guess()`. This causes string comparison instead of numeric comparison,
which breaks the win condition — guessing the correct number on an even
attempt would not register as a win correctly, and hint logic would also
malfunction.


## 2. How did you use AI as a teammate?
- I used github copilot for this project to identify where does the bug I realize come from and explain how does the "except TypeError:" part in check_guess work
- AI suggested me the code to reset the history, score, and status after hitting the new_game button 
- Luckily, all the suggestions AI gave me are all correct, so I don't have to deny any of them. 

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed? 
Ans: after I understand fully how does the new version of the code work and whether it pass all the test cases generated 
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
Ans: I ran test_guess_messages_are_correct() and test_reset_game_state_resets_session(monkeypatch) in pytest to test whether the first 2 bugs I realized (illogical message when I guess the wrong number and game not reset when I hit new_game) have been fixed or not 

- Did AI help you design or understand any tests? How?
Ans: AI helped me to designed the 2 aforementioned tests
---

  ## 4. What did you learn about Streamlit and state?
- The secret number kept changing because it was regenerated on every button click (rerun) instead of being stored in session state once at game start.
- Streamlit reruns the entire script on every user interaction, like button clicks, to update the UI; session state is a dictionary that persists data across these reruns, so variables like the secret stay the same unless you change them.
- I stored the secret in `st.session_state.secret` and initialized it only if not present, using the difficulty range, so it stays stable across guesses.

---

## 5. Looking ahead: your developer habits
- Writing unit tests with pytest and running them after changes to catch regressions.
- Ask AI for more specific code examples or explanations before implementing.
- This project showed me AI-generated code often has subtle bugs, so I now test thoroughly and refactor for clarity.
