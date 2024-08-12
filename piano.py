# import numpy as np
# import librosa
# import json
# import math
# import scipy.signal

# # 音高频率与音名对照表
# A4 = 440.0  # A4的频率
# C0 = A4 * pow(2,(12-69)/12)

# def check_p(hz):
#     hz = round(hz,2)
#     p = librosa.hz_to_midi(hz)
#     return p

# def pitch_to_note_name(pitch):
#     notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
#     octave = pitch // 12 - 1 
#     note = notes[math.floor(pitch % 12)]
#     return str(note) + str(octave)

# def delete_noise(sr, y):
#     highpass = scipy.signal.butter(10, 150, 'hp', fs=sr, output='sos')
#     y = scipy.signal.sosfilt(highpass, y)

#     lowpass = scipy.signal.butter(10, 4000, 'lp', fs=sr, output='sos')
#     y = scipy.signal.sosfilt(lowpass, y)

#     return y


# filename = '化成路29巷 8.wav'
# y, sr = librosa.load(filename)

# y = delete_noise(sr,y)

# # 使用librosa的音高检测功能
# pitches, magnitudes = librosa.core.piptrack(y=y, sr=sr)
# magnitude_threshold = 0.28* np.max(magnitudes) 

# notes = []  
# recent_notes = []  
# time_window = 0.015
# frames_per_window = int(time_window * sr / librosa.frames_to_samples(1, hop_length=128))

# for t in range(pitches.shape[1]):
#     index = magnitudes[:, t].argmax()
#     pitch = pitches[index, t]
#     # print(pitch)
#     # print(magnitudes[index, t])
#     magnitude = magnitudes[index, t]
#     if pitch > 0 and magnitude > magnitude_threshold :  # Only consider non-zero pitches
#         checked_pitch = check_p(pitch)
#         if checked_pitch:
#             note_name = pitch_to_note_name(checked_pitch)
#             if note_name:
#                 # 检查最近的音符记录中是否已经存在该音符
#                 if note_name not in recent_notes:
#                     notes.append(note_name)
#                     recent_notes.append(note_name)
#                 # 确保recent_notes不超过frames_per_window长度
#                 if len(recent_notes) > frames_per_window:
#                     recent_notes.pop(0)

# print(notes)

# # 去重并保存音名到 JSON 文件
# # unique_notes = list(set(notes))
# # print(unique_notes)
# # with open('notes.json', 'w') as f:
# #     json.dump(unique_notes, f)
import librosa
import numpy as np


# 加载音频文件
filename = '化成路29巷 6.wav'
y, sr = librosa.load(filename)
# beat_frequencies = []

notes = librosa.yin(y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'))
tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
beat_times = librosa.frames_to_time(beats, sr=sr)
# beat_times = librosa.frames_to_time(beats, sr=sr)
# for i in beat_times:
#     print(i)
#     i = i/2
#     window_size = 0.1

# for beat_time in beat_times:
#     # 确定窗口的开始和结束时间
#     start_time = max(0, beat_time - window_size / 2)
#     end_time = min(len(y) / sr, beat_time + window_size / 2)

#     # 将时间转换为样本索引
#     start_sample = int(start_time * sr)
#     end_sample = int(end_time * sr)

#     # 提取窗口内的音频片段
#     y_window = y[start_sample:end_sample]

#     # 计算该窗口内的频谱
#     D = np.abs(librosa.stft(y_window))
#     freqs = librosa.fft_frequencies(sr=sr)
    
#     # 计算频谱质心 (spectral centroid)
#     spectral_centroid = librosa.feature.spectral_centroid(S=D, sr=sr)
    
#     # 获取该窗口的平均频率
#     avg_freq = np.mean(spectral_centroid)
#     beat_frequencies.append(avg_freq)

# # 打印每个节拍的频率信息
# for i, freq in enumerate(beat_frequencies):
#     print(f"Beat {i+1}: Frequency = {freq:.2f} Hz")
    
print('notes: ', notes)
print('tempo: ', tempo) 
print('beats: ', beats)
print('beat_times: ', beat_times)

# # 使用librosa的音高检测功能
# pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
# time_window = 0.02
# frames_per_window = int(time_window * sr / librosa.frames_to_samples(1, hop_length=128))

# # 提取频率并转换为音名
# notes = []
# recent_notes = []
# for t in range(pitches.shape[1]):
#     index = magnitudes[:, t].argmax()
#     pitch = pitches[index, t]
#     if pitch > 0 and magnitudes[index, t] > 25:
#         print(pitch,magnitudes[index, t])
#         note_name = librosa.hz_to_note(pitch)
#         if note_name:
#                 # 检查最近的音符记录中是否已经存在该音符
#             if note_name not in recent_notes:
#                 notes.append(note_name)
#                 recent_notes.append(note_name)
#                 # print(note_name)
#             # 确保recent_notes不超过frames_per_window长度
#             if len(recent_notes) > frames_per_window:
#                 recent_notes.pop(0)

# print(notes)