# import librosa
# # import matplotlib.pyplot as plt
# import numpy as np
# import matplotlib.pyplot as plt

# # 读取音频文件
# filename = 'pianos-by-jtwayne-7-174717.wav'
# y, sr = librosa.load(filename) # y是音频数据，sr是采样率

# # # 计算音频的短时傅里叶变换（STFT）
# D = librosa.stft(y) # D是复数矩阵   
# DB = librosa.amplitude_to_db(abs(D), ref=np.max)    # 转换为幅度谱
# S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)



# # 绘制频谱图
# plt.figure(figsize=(12, 8))
# librosa.display.specshow(DB, sr=sr, x_axis='time', y_axis='log')
# plt.colorbar(format='%+2.0f dB')
# plt.title('Spectrogram')
# plt.show()

# # 提取梅尔频谱特征
# mel_spect = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
# mel_spect_db = librosa.amplitude_to_db(mel_spect, ref=np.max)

# # 绘制梅尔频谱图
# plt.figure(figsize=(12, 8))
# librosa.display.specshow(mel_spect_db, sr=sr, x_axis='time', y_axis='mel')
# plt.colorbar(format='%+2.0f dB')
# plt.title('Mel Spectrogram')
# plt.show()

# # 提取MFCC特征
# mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)

# # 绘制MFCC
# plt.figure(figsize=(12, 8))
# librosa.display.specshow(mfccs, sr=sr, x_axis='time')
# plt.colorbar()
# plt.title('MFCC')
# plt.show()

# # 节拍检测
# tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
# print('Estimated Tempo: {:.2f} BPM'.format(tempo))

# # 绘制节拍图
# plt.figure(figsize=(12, 8))
# plt.plot(librosa.times_like(beats, sr=sr), beats, 'r')
# plt.vlines(librosa.times_like(beats, sr=sr), 0, 1, color='r', alpha=0.5)
# plt.title('Beat Tracking')
# plt.show()


import numpy as np
import librosa
import json
import math
import scipy.signal

# 音高频率与音名对照表
A4 = 440.0  # A4的频率
C0 = A4 * pow(2,(12-69)/12)
# print(C0)

def check_p(hz):
    hz = round(hz,2)
    p = librosa.hz_to_midi(hz)
    return p

# print(check_p(440))

def pitch_to_note_name(pitch):
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    octave = pitch // 12 - 1
    note = notes[math.floor(pitch % 12)]
    return str(note) + str(octave)

# print(pitch_to_note_name(check_p(261.63)))


# 读取音频文件
filename = 'fxmf0-2chwg.wav'
y, sr = librosa.load(filename)

highpass = scipy.signal.butter(10, 150, 'hp', fs=sr, output='sos')
y = scipy.signal.sosfilt(highpass, y)

# 使用低通滤波器去除高频噪音
lowpass = scipy.signal.butter(10, 4000, 'lp', fs=sr, output='sos')
y = scipy.signal.sosfilt(lowpass, y)

# 使用librosa的音高检测功能
pitches, magnitudes = librosa.core.piptrack(y=y, sr=sr)
magnitude_threshold = 0.1* np.max(magnitudes)

# 提取频率并转换为音名
notes = []  # 用于存储检测到的音符

recent_notes = []  # 用于存储最近检测到的音符
time_window = 0.05 # 阈值时间，单位为秒
# print(librosa.frames_to_samples(1, hop_length=512))
frames_per_window = int(time_window * sr / librosa.frames_to_samples(1, hop_length=256))

for t in range(pitches.shape[1]):
    index = magnitudes[:, t].argmax()
    pitch = pitches[index, t]
    magnitude = magnitudes[index, t]
    if pitch > 0 and magnitude > magnitude_threshold :  # Only consider non-zero pitches
        checked_pitch = check_p(pitch)
        if checked_pitch:
            note_name = pitch_to_note_name(checked_pitch)
            if note_name:
                # 检查最近的音符记录中是否已经存在该音符
                if note_name not in recent_notes:
                    notes.append(note_name)
                    recent_notes.append(note_name)
                # 确保recent_notes不超过frames_per_window长度
                if len(recent_notes) > frames_per_window:
                    recent_notes.pop(0)

print(notes)

# # 去重并保存音名到 JSON 文件
# unique_notes = list(set(notes))
# with open('notes.json', 'w') as f:
#     json.dump(unique_notes, f)

# print("Detected Notes:", unique_notes)
# for t in range(pitches.shape[1]):
#     index = magnitudes[:, t].argmax()
#     pitch = pitches[index, t]
#     # print(pitch)
#     note_name = pitch_to_note_name(check_p(pitch))
#     if note_name:
#         notes.append(note_name)

# print(notes)