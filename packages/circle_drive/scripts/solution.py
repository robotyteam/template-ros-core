def solution(obs):
    import cv2
    import numpy as np
    import math
    img = cv2.cvtColor(np.ascontiguousarray(obs), cv2.COLOR_BGR2RGB)
    #img = np.ascontiguousarray(obs)
    rgb = img.copy()
    #flag = 1
    height = rgb.shape[0]
    width = rgb.shape[1]
    region_vertices = [
        (0, height),
        (0, height * 3 / 5),
        (width / 8, height / 2),
        (width * 7 / 8, height / 2),
        (width, height * 3 / 5),
        (width, height)
    ]
    if 'flag' not in globals():
        flag = 1
        return[0.25, 0]
    def region_of_interest(img, vertices):
        mask = np.zeros_like(img)
        ch_count = img.shape[2]
        match_mask_color = (255,) * ch_count
        cv2.fillPoly(mask, vertices, match_mask_color)
        masked_img = cv2.bitwise_and(img, mask)
        return masked_img

    cropped_img = region_of_interest(rgb, np.array([region_vertices], np.int32), )
    hsv = cv2.cvtColor(cropped_img, cv2.COLOR_RGB2HSV)
    
#     w_lane_min = np.array((73, 9, 120), np.uint8)
#     w_lane_max = np.array((146, 70, 255), np.uint8)

#     y_lane_min = np.array((0, 0, 114), np.uint8)
#     y_lane_max = np.array((52, 116, 255), np.uint8)
    
    w_lane_min = np.array((0, 0, 153), np.uint8)
    w_lane_max = np.array((180, 66, 255), np.uint8)

    y_lane_min = np.array((16, 80, 134), np.uint8)
    y_lane_max = np.array((23, 172, 227), np.uint8)

    w_lane = cv2.inRange(hsv, w_lane_min, w_lane_max)
    y_lane = cv2.inRange(hsv, y_lane_min, y_lane_max)
    
    w_lane_vector = cv2.Canny(w_lane, 100, 200)
    y_lane_vector = cv2.Canny(y_lane, 100, 200)
    w_lines = cv2.HoughLinesP(w_lane_vector, rho=6, theta=np.pi / 60, threshold=100,
                              lines=np.array([]), minLineLength=40, maxLineGap=25)
    y_lines = cv2.HoughLinesP(y_lane_vector, rho=6, theta=np.pi / 60, threshold=100,
                              lines=np.array([]), minLineLength=40, maxLineGap=25)
    #print ("White:", w_lines)
    #print ("Yellow:" , y_lines)
    w_angles = 0.0
    y_angles = 0.0
    w_line_pose_x = 0.0
    w_line_pose_y = 0.0
    w_line_pose_x1 = 0.0
    w_line_pose_x2 = 0.0
    w_line_pose_y1 = 0.0
    w_line_pose_y2 = 0.0
    y_line_pose_x = 0.0
    y_line_pose_y = 0.0
    y_line_pose_x1 = 0.0
    y_line_pose_x2 = 0.0
    y_line_pose_y1 = 0.0
    y_line_pose_y2 = 0.0
    try:
        counter = 0
        angles = 0.0
        y_line_pose = 0
        for line in y_lines:
            for x1, y1, x2, y2 in line:
                cv2.line(rgb, (x1, y1), (x2, y2), (0, 255, 0), thickness=2)
                if (y2 > y1):
                    tmpX = x1
                    tmpY = y1
                    x1 = x2
                    y1 = y2
                    x2 = tmpX
                    y2 = tmpY
                dX = x2 - x1
                dY = y2 - y1
                mod = math.sqrt(dX ** 2 + dY ** 2)
                angle = math.degrees(math.acos(dX / mod))
                y_line_pose_x1 = y_line_pose_x1 + x1
                y_line_pose_x2 = y_line_pose_x2 + x2
                y_line_pose_y1 = y_line_pose_y1 + y1
                y_line_pose_y2 = y_line_pose_y2 + y2
                angles += angle
                counter += 1
                y_line_pose = y_line_pose + x1 + x2
                # print ("yellow" , line ,  angle)
        y_angles = angles / counter
        y_line_pose_x1 = int(y_line_pose_x1 / counter)
        y_line_pose_x2 = int(y_line_pose_x2 / counter)
        y_line_pose_y1 = int(y_line_pose_y1 / counter)
        y_line_pose_y2 = int(y_line_pose_y2 / counter)
        y_line_pose_x = (y_line_pose_x1 + y_line_pose_x2) / 2
        y_line_pose_y = (y_line_pose_y1 + y_line_pose_y2) / 2
        cv2.line(rgb, (y_line_pose_x1, y_line_pose_y1), (y_line_pose_x2, y_line_pose_y2),
                 (50, 50, 125), thickness=5)
    except:
        y_angles = 0
    try:
        counter = 0
        angles = 0.0
        for line in w_lines:
            for x1, y1, x2, y2 in line:
                if x1>320:
                    if (y2 > y1):
                        tmpX = x1
                        tmpY = y1
                        x1 = x2
                        y1 = y2
                        x2 = tmpX
                        y2 = tmpY
                    dX = x2 - x1
                    dY = y2 - y1
                    mod = math.sqrt(dX ** 2 + dY ** 2)
                    angle = math.degrees(math.acos(dX / mod))
                    if y1 > height / 3 and x1 > width / 3:
                        cv2.line(rgb, (x1, y1), (x2, y2), (255, 255, 0), thickness=2)
                    w_line_pose_x1 = w_line_pose_x1 + x1
                    w_line_pose_x2 = w_line_pose_x2 + x2
                    w_line_pose_y1 = w_line_pose_y1 + y1
                    w_line_pose_y2 = w_line_pose_y2 + y2
                    angles += angle
                    counter += 1
                    # print ("white" ,line , angle)
        w_angles = angles / counter
        w_line_pose_x1 = int(w_line_pose_x1 / counter)
        w_line_pose_x2 = int(w_line_pose_x2 / counter)
        w_line_pose_y1 = int(w_line_pose_y1 / counter)
        w_line_pose_y2 = int(w_line_pose_y2 / counter)
        w_line_pose_x = (w_line_pose_x1 + w_line_pose_x2) / 2
        w_line_pose_y = (w_line_pose_y1 + w_line_pose_y2) / 2
        cv2.line(rgb, (w_line_pose_x1, w_line_pose_y1), (w_line_pose_x2, w_line_pose_y2),
                 (125, 50, 50), thickness=5)
    except:
        w_angles = 0
    # cv2.imshow('111',rgb)
    # cv2.waitKey()

    #print(w_line_pose_x, y_line_pose_x)
    w_need = 590
    y_need = 130
    if w_line_pose_x > 0:
        w_deviation = w_line_pose_x - w_need
    else:
        w_deviation = 82
    if y_line_pose_x > 0:
        y_deviation = y_line_pose_x - y_need
    else:
        y_deviation = -82

    pose = -(w_deviation + y_deviation) / 1000
    kP = 6.5  # основной коэффициент усиления поворота колес
    if y_line_pose_y > 370 and y_angles < 32:
        kP = 7.5  # коэффициент, если обнаружена желтая разметка почти горизонтально близко к роботу
    steering = kP * pose
    if 'average_pose' not in globals():
            average_pose = []
    if len(average_pose) < 6:  # количество элементов для вычисления среднего значения поворота руля
        average_pose.append(steering)
    else:
        average_pose.pop(0)
        average_pose.append(steering)
        steering = 0
        for i in range(len(average_pose)):
            steering += average_pose[i]
        steering = steering / len(average_pose)
    
    if -0.12 < steering < 0.12 and steering != 0:
        vel = 0.3  # ускоряемся при движении прямо
        steering = steering * 0.98  # и корректируем руль на большой скорости
    else:
        vel = 0.25  # скорость во время поворота
    print("steering", steering,"speed",vel)
    return [vel, steering]
