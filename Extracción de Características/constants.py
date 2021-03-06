JOINT_NUM = 15
# JOINT_NUM = 20
CSV_DELIMITER = ','

# JOINTS = ['HEAD','NECK','TORSO','LEFT_SHOULDER','LEFT_ELBOW','RIGHT_SHOULDER','RIGHT_ELBOW','LEFT_HIP','LEFT_KNEE','RIGHT_HIP','RIGHT_KNEE','LEFT_HAND','RIGHT_HAND','LEFT_FOOT','RIGHT_FOOT']

# BASE_SPINE = 0
# MIDDLE_SPINE = 1
# NECK = 2
# HEAD = 3
# LEFT_SHOULDER = 4
# LEFT_ELBOW = 5
# LEFT_WRIST = 6
# LEFT_HAND = 7
# RIGHT_SHOULDER = 8
# RIGHT_ELBOW = 9
# RIGHT_WRIST = 10
# RIGHT_HAND = 11
# LEFT_HIP = 12
# LEFT_KNEE = 13
# LEFT_ANKLE = 14
# LEFT_FOOT = 15
# RIGHT_HIP = 16
# RIGHT_KNEE = 17
# RIGHT_ANKLE = 18
# RIGHT_FOOT = 19

# CONEXION_GRAPH = {
#     BASE_SPINE: [MIDDLE_SPINE, LEFT_HIP, RIGHT_HIP],
#     MIDDLE_SPINE: [BASE_SPINE, NECK],
#     NECK: [MIDDLE_SPINE, HEAD],
#     HEAD: [NECK],
#     LEFT_SHOULDER: [LEFT_ELBOW, RIGHT_SHOULDER],
#     LEFT_ELBOW: [LEFT_SHOULDER, LEFT_WRIST],
#     LEFT_WRIST: [LEFT_ELBOW, LEFT_HAND],
#     LEFT_HAND: [LEFT_WRIST],
#     RIGHT_SHOULDER: [LEFT_SHOULDER, RIGHT_ELBOW],
#     RIGHT_ELBOW: [RIGHT_SHOULDER, RIGHT_WRIST],
#     RIGHT_WRIST: [RIGHT_ELBOW, RIGHT_HAND],
#     RIGHT_HAND: [RIGHT_WRIST],
#     LEFT_HIP: [BASE_SPINE, LEFT_KNEE],
#     LEFT_KNEE: [LEFT_HIP, LEFT_ANKLE],
#     LEFT_ANKLE: [LEFT_KNEE, LEFT_FOOT],
#     LEFT_FOOT: [LEFT_ANKLE],
#     RIGHT_HIP: [BASE_SPINE, RIGHT_KNEE],
#     RIGHT_KNEE: [RIGHT_HIP, RIGHT_ANKLE],
#     RIGHT_ANKLE: [RIGHT_KNEE, RIGHT_FOOT],
#     RIGHT_FOOT: [RIGHT_ANKLE],
# }

# VELOCITY_JOINTS = [MIDDLE_SPINE, LEFT_HAND, RIGHT_HAND, LEFT_FOOT, RIGHT_FOOT]

HEAD = 0
NECK = 1
LEFT_SHOULDER = 2
RIGHT_SHOULDER = 3
LEFT_ELBOW = 4
RIGHT_ELBOW = 5
LEFT_HAND = 6
RIGHT_HAND = 7
TORSO = 8
LEFT_HIP = 9
RIGHT_HIP = 10
LEFT_KNEE = 11
RIGHT_KNEE = 12
LEFT_FOOT = 13
RIGHT_FOOT = 14

CONEXION_GRAPH = {
    HEAD: [NECK],
    NECK: [HEAD],
    LEFT_SHOULDER: [LEFT_ELBOW, RIGHT_SHOULDER, TORSO],
    RIGHT_SHOULDER: [RIGHT_ELBOW, LEFT_SHOULDER, TORSO],
    LEFT_ELBOW: [LEFT_SHOULDER, LEFT_HAND],
    RIGHT_ELBOW: [RIGHT_SHOULDER, RIGHT_HAND],
    LEFT_HAND: [LEFT_ELBOW],
    RIGHT_HAND: [RIGHT_ELBOW],
    TORSO: [LEFT_SHOULDER, RIGHT_SHOULDER, LEFT_HIP, RIGHT_HIP],
    LEFT_HIP: [TORSO, RIGHT_HIP, LEFT_KNEE],
    RIGHT_HIP: [TORSO, LEFT_HIP, RIGHT_KNEE],
    LEFT_KNEE: [LEFT_HIP, LEFT_FOOT],
    RIGHT_KNEE: [RIGHT_HIP, RIGHT_FOOT],
    LEFT_FOOT: [LEFT_KNEE],
    RIGHT_FOOT: [RIGHT_KNEE],
}

VELOCITY_JOINTS = [TORSO, LEFT_HAND, RIGHT_HAND, LEFT_FOOT, RIGHT_FOOT]

FRAMES_PER_SECOND = 30
FRAME_TIME = 1/FRAMES_PER_SECOND
