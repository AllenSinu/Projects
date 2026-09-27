import cv2
import mediapipe as mp
import random
import time

from gesture import detect_gesture


# ==========================================
# MEDIAPIPE SETUP
# ==========================================

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)


# ==========================================
# CAMERA SETUP
# ==========================================

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Could not access camera")
    exit()


# ==========================================
# GAME VARIABLES
# ==========================================

player_score = 0
computer_score = 0

target_score = 2

game_started = False
game_over = False

countdown_active = False
countdown_start = 0

result_text = ""

player_gesture = "Waiting..."
computer_gesture = "Waiting..."

round_number = 1


# ==========================================
# FUNCTIONS
# ==========================================

def computer_move():
    return random.choice([
        "Rock",
        "Paper",
        "Scissors"
    ])


def determine_winner(player, computer):

    if player == computer:
        return "Draw"

    if (
        player == "Rock"
        and computer == "Scissors"
    ):
        return "Player"

    if (
        player == "Paper"
        and computer == "Rock"
    ):
        return "Player"

    if (
        player == "Scissors"
        and computer == "Paper"
    ):
        return "Player"

    return "Computer"


def reset_game():

    global player_score
    global computer_score
    global game_started
    global game_over
    global countdown_active
    global countdown_start
    global result_text
    global player_gesture
    global computer_gesture
    global round_number

    player_score = 0
    computer_score = 0

    game_started = True
    game_over = False

    countdown_active = True
    countdown_start = time.time()

    result_text = ""

    player_gesture = "Waiting..."
    computer_gesture = "Waiting..."

    round_number = 1


# ==========================================
# MAIN LOOP
# ==========================================

while True:

    ret, frame = cap.read()

    if not ret:
        print("Could not read camera")
        break


    # Mirror camera
    frame = cv2.flip(frame, 1)


    # Convert BGR to RGB
    rgb_frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )


    # MediaPipe hand detection
    results = hands.process(rgb_frame)


    # Default gesture
    gesture = "No hand"


    # ==========================================
    # HAND DETECTION
    # ==========================================

    if results.multi_hand_landmarks:

        hand = results.multi_hand_landmarks[0]

        # Draw hand landmarks
        mp_draw.draw_landmarks(
            frame,
            hand,
            mp_hands.HAND_CONNECTIONS
        )

        # Detect Rock / Paper / Scissors
        gesture = detect_gesture(
            hand.landmark
        )


    # ==========================================
    # MAIN MENU
    # ==========================================

    if not game_started:

        cv2.putText(
            frame,
            "ROCK PAPER SCISSORS",
            (70, 100),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.2,
            (0, 255, 255),
            3
        )

        cv2.putText(
            frame,
            "Press 3 = Best of 3",
            (120, 180),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (255, 0, 0),
            2
        )

        cv2.putText(
            frame,
            "Press 5 = Best of 5",
            (120, 230),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (255, 0, 0),
            2
        )

        cv2.putText(
            frame,
            "Press Q = Quit",
            (120, 280),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )


    # ==========================================
    # GAME
    # ==========================================

    else:

        # --------------------------------------
        # SCORE
        # --------------------------------------

        cv2.putText(
            frame,
            f"YOU: {player_score}",
            (30, 45),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"COMPUTER: {computer_score}",
            (350, 45),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"ROUND: {round_number}",
            (240, 85),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 0, 0),
            2
        )


        # ======================================
        # COUNTDOWN
        # ======================================

        if countdown_active and not game_over:

            elapsed = time.time() - countdown_start


            # 3
            if elapsed < 1:

                countdown_text = "3"


            # 2
            elif elapsed < 2:

                countdown_text = "2"


            # 1
            elif elapsed < 3:

                countdown_text = "1"


            # SHOW
            elif elapsed < 3.5:

                countdown_text = "SHOW"


            # Countdown finished
            else:

                countdown_active = False

                # Check if gesture is valid
                if gesture in [
                    "Rock",
                    "Paper",
                    "Scissors"
                ]:

                    player_gesture = gesture

                    computer_gesture = computer_move()

                    result = determine_winner(
                        player_gesture,
                        computer_gesture
                    )


                    # --------------------------
                    # UPDATE SCORE
                    # --------------------------

                    if result == "Player":

                        player_score += 1

                        result_text = "YOU WIN!"


                    elif result == "Computer":

                        computer_score += 1

                        result_text = "COMPUTER WINS!"


                    else:

                        result_text = "DRAW!"


                    # --------------------------
                    # CHECK GAME OVER
                    # --------------------------

                    if player_score >= target_score:

                        game_over = True

                        result_text = "YOU WON THE GAME!"


                    elif computer_score >= target_score:

                        game_over = True

                        result_text = "COMPUTER WON THE GAME!"


                else:

                    result_text = "NO GESTURE DETECTED"


                # Move to next round
                if not game_over:

                    round_number += 1

                    countdown_start = time.time()


            # Display countdown
            if countdown_active:

                cv2.putText(
                    frame,
                    countdown_text,
                    (250, 250),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    3,
                    (0, 255, 255),
                    5
                )


        # ======================================
        # RESULT SCREEN
        # ======================================

        else:

            cv2.putText(
                frame,
                "YOU: " + player_gesture,
                (30, 145),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 0, 0),
                2
            )

            cv2.putText(
                frame,
                "COMPUTER: " + computer_gesture,
                (30, 185),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 0, 0),
                2
            )

            cv2.putText(
                frame,
                result_text,
                (80, 300),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                (0, 255, 255),
                3
            )


            # ----------------------------------
            # GAME OVER
            # ----------------------------------

            if game_over:

                cv2.putText(
                    frame,
                    "GAME OVER",
                    (180, 360),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.0,
                    (0, 0, 255),
                    3
                )

                cv2.putText(
                    frame,
                    "Press R to restart",
                    (150, 410),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 255, 255),
                    2
                )


            # ----------------------------------
            # START NEXT ROUND
            # ----------------------------------

            else:

                # Wait 2 seconds
                if time.time() - countdown_start > 2:

                    countdown_active = True

                    countdown_start = time.time()


    # ==========================================
    # DETECTED GESTURE
    # ==========================================

    if not game_over:

        cv2.putText(
            frame,
            "Detected: " + gesture,
            (30, 450),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )


    # ==========================================
    # DISPLAY WINDOW
    # ==========================================

    cv2.imshow(
        "Rock Paper Scissors",
        frame
    )


    # ==========================================
    # KEYBOARD CONTROLS
    # ==========================================

    key = cv2.waitKey(1) & 0xFF


    # Best of 3
    if key == ord("3"):

        target_score = 2

        reset_game()


    # Best of 5
    elif key == ord("5"):

        target_score = 3

        reset_game()


    # Restart after game over
    elif key == ord("r"):

        if game_over:

            reset_game()


    # Quit
    elif key == ord("q"):

        break


# ==========================================
# CLEANUP
# ==========================================

cap.release()

cv2.destroyAllWindows()