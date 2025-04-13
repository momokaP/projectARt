import numpy as np
import cv2 as cv

# === 비디오 파일 및 카메라 보정값 ===
video_file = './KakaoTalk_20250405_210903239.mp4'
output_file = './output_sphere_wireframe.mp4'

K = np.array([[645.74279809, 0, 629.74120962],
              [0, 655.30770132, 393.42013333],
              [0, 0, 1]])
dist_coeff = np.array([-0.01799652, 0.19082015, -0.00970454, 0.00211079, -0.2281721])

# === 체스보드 설정 ===
board_pattern = (10, 7)
board_cellsize = 0.023
board_criteria = cv.CALIB_CB_ADAPTIVE_THRESH + cv.CALIB_CB_NORMALIZE_IMAGE + cv.CALIB_CB_FAST_CHECK

video = cv.VideoCapture(video_file)
assert video.isOpened(), 'Cannot read the given input, ' + video_file

# 영상 크기와 fps 정보
frame_width = int(video.get(cv.CAP_PROP_FRAME_WIDTH))
frame_height = int(video.get(cv.CAP_PROP_FRAME_HEIGHT))
fps = video.get(cv.CAP_PROP_FPS)

# === 영상 저장을 위한 VideoWriter 설정 ===
fourcc = cv.VideoWriter_fourcc(*'mp4v')
out = cv.VideoWriter(output_file, fourcc, fps, (frame_width, frame_height))

# === 체스보드 월드 좌표계 상의 포인트 ===
obj_points = board_cellsize * np.array([[c, r, 0] for r in range(board_pattern[1]) for c in range(board_pattern[0])])

# === 구 설정 ===
sphere_center = board_cellsize * np.array([4.5, 3.5, -0.5])
sphere_radius = 0.02

# === 구 포인트 + 선 생성 함수 ===
def create_sphere_points_with_lines(center, radius, num_lat=10, num_lon=20):
    points = []
    lines = []

    for i in range(1, num_lat):
        lat = np.pi * i / num_lat
        for j in range(num_lon):
            lon = 2 * np.pi * j / num_lon
            x = radius * np.sin(lat) * np.cos(lon)
            y = radius * np.sin(lat) * np.sin(lon)
            z = radius * np.cos(lat)
            points.append(center + np.array([x, y, z]))

    for i in range(num_lat - 1):
        for j in range(num_lon):
            curr = i * num_lon + j
            next_j = i * num_lon + (j + 1) % num_lon
            lines.append((curr, next_j))

    for i in range(num_lat - 2):
        for j in range(num_lon):
            curr = i * num_lon + j
            below = (i + 1) * num_lon + j
            lines.append((curr, below))

    return np.array(points), lines

sphere_3d, sphere_lines = create_sphere_points_with_lines(sphere_center, sphere_radius)

# === 메인 루프 ===
while True:
    valid, img = video.read()
    if not valid:
        break

    success, img_points = cv.findChessboardCorners(img, board_pattern, board_criteria)
    if success:
        ret, rvec, tvec = cv.solvePnP(obj_points, img_points, K, dist_coeff)
        projected_pts, _ = cv.projectPoints(sphere_3d, rvec, tvec, K, dist_coeff)
        projected_pts = np.int32(projected_pts).reshape(-1, 2)

        for i, j in sphere_lines:
            pt1 = tuple(projected_pts[i])
            pt2 = tuple(projected_pts[j])
            cv.line(img, pt1, pt2, (255, 100, 100), 1)

        R, _ = cv.Rodrigues(rvec)
        p = (-R.T @ tvec).flatten()
        info = f'XYZ: [{p[0]:.3f} {p[1]:.3f} {p[2]:.3f}]'
        cv.putText(img, info, (10, 25), cv.FONT_HERSHEY_DUPLEX, 0.6, (0, 255, 0))

    # === 화면 표시 및 저장 ===
    cv.imshow('Pose Estimation with Sphere (Wireframe)', img)
    out.write(img)  # 저장

    key = cv.waitKey(10)
    if key == ord(' '):
        key = cv.waitKey()
    if key == 27:
        break

video.release()
out.release()
cv.destroyAllWindows()
