from flask import Flask,request,jsonify
import librosa
import io
import numpy as np
import json
from datetime import datetime
import cv2
import matplotlib.pyplot as plt


app = Flask(__name__)

@app.route('/audio_process', methods=['POST'])
def process_audio():
    if not request.data:
        return "No data received", 400

    audio_data = request.data
    
    # Process audio data here
    y, sr = librosa.load(io.BytesIO(audio_data), sr=None)
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beats, sr=sr)

    # check pitch
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    time_window = 0.02
    frames_per_window = int(time_window * sr / librosa.frames_to_samples(1, hop_length=128))

    # detect notes
    notes = []
    recent_notes = []
    for t in range(pitches.shape[1]):
        index = magnitudes[:, t].argmax()
        pitch = pitches[index, t]
        if pitch > 0 and magnitudes[index, t] > 25:
            # print(pitch,magnitudes[index, t])
            note_name = librosa.hz_to_note(pitch)
            if note_name:
                note_name = note_name.replace('♯', '')
                    # 检查最近的音符记录中是否已经存在该音符
                if note_name not in recent_notes:
                    
                    notes.append(note_name)
                    recent_notes.append(note_name)
                    
                #確保最近的音符記錄不會超過frame大小        
                if len(recent_notes) > frames_per_window:
                    recent_notes.pop(0)

    
    # print(type(beats))
    # print(type(tempo))

    response = {
        'notes': notes,
        'tempo': tempo.tolist(),
        'beats': beats.tolist(),
        'timeStamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'beat_times': beat_times.tolist()
    }
    return response

@app.route('/image_process', methods=['POST'])
def process_image():
    # if not request.data:
    #     return "No data received", 400

    image_file = request.files['image']
    image_data = np.fromfile(image_file, np.uint8)
    image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
    image = cv2.rectangle(image, (0, 0), (2499, 475), (255, 255, 255), -1)
    image = cv2.rectangle(image, (0, 480), (580, 910), (255, 255, 255), -1)
    image = cv2.rectangle(image, (0, 1000), (290, 3499), (255, 255, 255), -1)
    image = cv2.rectangle(image, (0, 1500), (260, 2000), (255, 255, 255), -1)
    image = cv2.rectangle(image, (0, 3250), (2499, 3499), (255, 255, 255), -1)
    blurred_image_path = 'images\starr.jpg'
    cv2.imwrite(blurred_image_path, image)
    cv2.waitKey(0)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    circles = cv2.HoughCircles(
        gray,
        cv2.HOUGH_GRADIENT,
        dp=1,
        minDist=30,
        param1=75,
        param2=12.5,
        minRadius=8,
        maxRadius=20
    )

    note_line_1=[]
    note_line_2=[]
    note_line_3=[]
    note_line_4=[]
    note_line_5=[]
    note_line_6=[]
    note1 = []
    note2 = []
    note3 = []  
    note4 = []
    note5 = []
    note6 = []
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            # 绘制外圆
            print(i)
            cv2.circle(image, (i[0], i[1]), i[2], (0, 255, 0), 2)
            # 绘制圆心
            cv2.circle(image, (i[0], i[1]), 2, (0, 0, 255), 3)
            if(i[1]>500 and i[1]<750):
                note_line_1.append(i)
            elif(i[1]>750 and i[1]<1000):
                note_line_2.append(i)
            elif(i[1]>1000 and i[1]<1250):
                note_line_3.append(i)
            elif(i[1]>1250 and i[1]<1500):
                note_line_4.append(i)
            elif(i[1]>1500 and i[1]<1750 and i[0]<2250):
                note_line_5.append(i)
            elif(i[1]>1750 and i[1]<2000 and i[0]<2250):
                note_line_6.append(i)
            else:
                continue
    plt.imshow(image)
    plt.show()

    note_line_1.sort(key=lambda x: x[0]+x[1])
    note_line_2.sort(key=lambda x: x[0]+x[1])
    note_line_3.sort(key=lambda x: x[0]+x[1])  
    note_line_4.sort(key=lambda x: x[0]+x[1])
    note_line_5.sort(key=lambda x: x[0]+x[1])
    note_line_6.sort(key=lambda x: x[0]+x[1])
    for i in note_line_1:
        note1.append(int(i[0]))
    for i in note_line_2:
        note2.append(int(i[0]))
    for i in note_line_3:
        note3.append(int(i[0]))
    for i in note_line_4:
        note4.append(int(i[0]))
    for i in note_line_5:
        note5.append(int(i[0]))
    for i in note_line_6:
        note6.append(int(i[0]))

    print(len(note1))
    print(len(note3))
    print(len(note5))

    response = {
        'note1': note1,
        'note2': note2,
        'note3': note3,
        'note4': note4,
        'note5': note5,
        'note6': note6,
        # 'timeStamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    return response


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
