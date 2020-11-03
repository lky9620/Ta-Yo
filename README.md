# 라즈베리파이를 이용한 교육용 자율주행 자동차 개발
## Self-driving  Model Car with RPi
### 주요 기능 및 작동 방식
+ 실시간 차선 인식을 통한 차로이탈 방지 
+ 신호등, 표지판등의 객체 인식을 통한 자율주행
+ 초음파 센서를 이용한 긴급 제동
+ GPU 서버와의 실시간 소켓통신을 통한 RPi의 성능 한계 극복
### 실시간 차선 인식(with OpenCV in RPi)
+ 차선 인식 과정 : Gray - Canny - ROI - HoughLines - Weighted
  + Gray(흑백화)
  ```python
  gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
  ```
  <p align = "center"><img width = "50%" src = "https://user-images.githubusercontent.com/61020702/97960342-a0af4980-1df4-11eb-9ca0-42c873c7bb8d.png"></p>
  
  + Canny(모서리 검출): Canny 알고리즘 이용.
  ```python
  can = cv2.Canny(gray, 50, 200, None, 3)
  ```
  <p align = "center"><img width = "50%" src = "https://user-images.githubusercontent.com/61020702/97960348-a3aa3a00-1df4-11eb-949e-bbf1708c6c95.png"></p>
  
  + ROI(Region of Interst, 관심 구역 설정)
  ```python
  rectangle = np.array([[(0, height), (120, 300), (520, 300), (640, height)]]) #[upper_left, lower_left, upper_right, lower_right]
  ```
  <p align = "center"><img width = "50%" src = "https://user-images.githubusercontent.com/61020702/97960350-a60c9400-1df4-11eb-8289-d5575eee4a0b.png"></p>
  
  + HoughLines(직선 검출)
  ```python
  line_arr = cv2.HoughLinesP(masked_image, 1, np.pi / 180, 20, minLineLength=10, maxLineGap=10)
  ```
  <p align = "center"><img width = "50%" src = "https://user-images.githubusercontent.com/61020702/97960354-a73dc100-1df4-11eb-8fd5-808a5c7cd416.png"></p>
  
  + Weighted(원본 영상에 합성)
  ```python
  mimg = cv2.addWeighted(src, 1, ccan, 1, 0)
  ```
  <p align = "center"><img width = "50%" src = https://user-images.githubusercontent.com/61020702/97960357-aa38b180-1df4-11eb-852d-24eb4e3aeb09.png></p>
  
+ 차선 인식 알고리즘
  ```python
  def DetectLineSlope(src):
  ...
  return mimg, degree_L, degree_R ## 대표선이 그려진 영상의 프레임, 왼쪽 대표선의 기울기, 오른쪽 대표선의 기울기
  ```
  + 대표선 추출: /Raspberry-Pi/line_detect.py의 DetectLineSlope(src)에 정의, 인식 되는 양 차선의 안쪽차선을 대표선으로 결정.
  + 대표선의 기울기 구하기: 대표선으로 차선으로 인식되는 직선의 좌표(x1,y1,x2,y2)를 통해 왼쪽, 오른쪽 대표선의 기울기를 구함, 인식되는 차선이 없을 경우 0을 반환.
  + line_detect.py(예제)의 알고리즘 흐름도 
  <p align = "center"><img width = "70%" src =https://user-images.githubusercontent.com/61020702/97975014-cac03600-1e0b-11eb-87da-eb07428c5de4.JPG></p>
  
+ 실습
  1. RPi(Rasbian)에 예제 소스코드 복제
  ``` 
  $ git clone https://github.com/lky9620/Ta-Yo.git
  ```
  2. Raspberry-Pi 디렉토리로 이동
  ``` 
  $ cd /Ta-Yo/Raspberry-Pi 
  ```
  3. 자신의 환경에 맞게 servo.py, line_detect.py 수정 후 실행
  
  ``` 
  ~Ta-Yo/Raspberry-Pi$ python line_detect.py
  ```
  or
   ``` 
  ~Ta-Yo/Raspberry-Pi$ python3 line_detect.py
  ```
+ 실습 동영상

 [![SelfDriving Car](https://img.youtube.com/vi/R1AdUfwLoxI/0.jpg)](https://youtu.be/R1AdUfwLoxI?t=0s)


### Yolo를 이용한 신호등, 표지판 등의 객체인식
+ Yolo(실시간 객체 인식)을 통해서 청색, 적색 신호등, 사람, 여러 표지판 등을 미리 학습하여 가중치 모델(학습 모델) 생성.
++ 방법은 추후에 notebook 파일 업로드 예정
++ 데이터셋은 저작권 등의 문제로 비공개
+
###
``` 
$git clone https://github.com/lky9620/Ta-Yo//Raspberry-Pi
```
