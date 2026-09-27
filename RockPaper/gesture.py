def detect_gesture(landmarks):

    # Index finger
    index_up = landmarks[8].y < landmarks[6].y

    # Middle finger
    middle_up = landmarks[12].y < landmarks[10].y

    # Ring finger
    ring_up = landmarks[16].y < landmarks[14].y

    # Pinky finger
    pinky_up = landmarks[20].y < landmarks[18].y

    fingers = [
        index_up,
        middle_up,
        ring_up,
        pinky_up
    ]

    count = sum(fingers)

    # Rock
    if count == 0:
        return "Rock"

    # Paper
    elif count == 4:
        return "Paper"

    # Scissors
    elif index_up and middle_up and not ring_up and not pinky_up:
        return "Scissors"

    return "Unknown"