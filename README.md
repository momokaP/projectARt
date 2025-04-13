# projectARt
projectARt 는 체스보드를 인식해 카메라의 자세(pose)를 추정하고, 체스보드 위에 3D 와이어프레임 구를 투영하는 컴퓨터 비전 프로젝트입니다.  OpenCV 기반으로 카메라 보정, PnP 문제 해결, 3차원 점 투영을 다루며, 증강현실(AR)이나 비전 기술 학습 및 데모용입니다.

프로그램 및 기능 설명

- 카메라 캘리브레이션 결과를 받아서 체스보드 패턴을 통해 카메라 포즈(자세) 추정

- 월드 좌표계에 위치한 3D 구를 투영하여 이미지 위에 그리기

- 처리된 결과를 동영상으로 저장 및 실시간 출력

# Camera pose estimation

카메라 영상

https://github.com/user-attachments/assets/2ba031a7-a920-4d49-ac0f-e194e65a7148

```
# 카메라 캘리브레이션 값
K = np.array([[645.74279809, 0, 629.74120962],
              [0, 655.30770132, 393.42013333],
              [0, 0, 1]])
dist_coeff = np.array([-0.01799652, 0.19082015, -0.00970454, 0.00211079, -0.2281721])
```

```
# 포즈 추정
ret, rvec, tvec = cv.solvePnP(obj_points, img_points, K, dist_coeff)
```

![pe](https://github.com/user-attachments/assets/35080760-88a7-4cb5-8265-d56f82e0d784)


# ARobject visualization

AR 물체 표시 결과 데모

https://github.com/user-attachments/assets/2cf3f432-c005-4d57-ae76-6ebed941659e

