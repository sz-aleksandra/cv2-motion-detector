import cv2  # to trzeba pobrać
from datetime import datetime, timedelta
import winsound  # to działa tylko na windowsie
from office_schedule import get_closed_days, read_hours

# to się raczej nie zmieni
RECORDING_COOLDOWN = 30  # w minutach
FRAMES_TO_RECORD = 200


def read_settings():
    '''
    wczytuje ustawienia z pliku
    '''
    with open('detection_sensibility_and_factor.txt', 'r') as file_handle:
        data = file_handle.readline()
        sensibility, frames_to_light_lights, factor = data.split(', ')
    return sensibility, frames_to_light_lights, factor


def read_and_process_frame(video):
    '''
    pobiera klatkę bluruje ją i zmienia na czarnobiałą,
    zmniejsza efekt małych ruchów i zmiany warunkow oświetleniowych
    '''
    _, frame = video.read()
    frame_processed = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_processed = cv2.GaussianBlur(frame_processed, (3, 3), 0)
    H = len(frame_processed)
    W = len(frame_processed[0])
    return frame, frame_processed, W, H


def detect_movement():
    '''
    wykrywa ruch i nagrywa jeśli jest on w godzinach zamkniecia biura

    dokladniej to liczy ile klatek z dziesięciu jest znacząco różnych
    sprawdza jest ich więcej niż wczytany limit
    '''
    last_movement = datetime.now() - timedelta(minutes=RECORDING_COOLDOWN)
    frames_with_movement_in_cycle = 0  # cykl ma 10 klatek
    count_frames_in_cycle = 0
    frames_recorded = FRAMES_TO_RECORD + 1  # wyzerowane po wykryciu ruchu w godzinach zamknięcia
    video = cv2.VideoCapture(0)  # znowu na moim komputerze; u znajomego cv2.CAP_V4L2
    sensibility, frames_to_light_lights, factor = read_settings()
    opening, _, closing = read_hours()
    _, last_frame_processed, W, H = read_and_process_frame(video)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    output = None
    while True:
        frame, frame_processed, _, _ = read_and_process_frame(video)
        frames_diff = cv2.absdiff(last_frame_processed, frame_processed)
# fajny bajer wyświetla krawędzie poruszających się obiektów i potem pozwala na zakończenie programu
        cv2.imshow('motion detection', frames_diff)
        sum_diffrences = sum(sum(x > int(sensibility) for x in frames_diff))
# tu można sprawdzić przez ile klatek wykrywany jest ruch podczas zapalania światła
#        print(sum_diffrences)
        count_frames_in_cycle += 1
        if sum_diffrences > float(factor) * W * H:
            frames_with_movement_in_cycle = frames_with_movement_in_cycle + 1
        if count_frames_in_cycle == 10:
            if frames_with_movement_in_cycle > int(frames_to_light_lights):
                count_frames_in_cycle = 0
                frames_with_movement_in_cycle = 0
                print('Moving!')
#                print('\a')
#                sys.stdout.write('\a')
#ktores z powyzszych powinno działać, ale u mnie nie słychać 
#to fajen bo można ustawiać długość więc się tak nie zacina, ale tylko windows
                winsound.Beep(2000, 100)
#to do kazdego systemu, ale nie można ustawiać długości i trzeba pobrać beepy
#                beep(sound='ping')
                current_time = datetime.now()
                if current_time.weekday() in get_closed_days() or current_time.hour >= closing or current_time.hour < opening:
                    if current_time - last_movement > timedelta(minutes=RECORDING_COOLDOWN):
                        frames_recorded = 0
                        file_name = (current_time.strftime('%Y-%m-%d_%H-%M'))
                        output = cv2.VideoWriter("movement_detected_on_" + f"{file_name}" + ".avi", fourcc, 20, (640, 480))
            count_frames_in_cycle = 0
            frames_with_movement_in_cycle = 0
        if frames_recorded <= FRAMES_TO_RECORD:
            last_movement = current_time
            output.write(frame)
            frames_recorded += 1
        last_frame_processed = frame_processed
# pozwala na zamknięcie programu w inny sposób niż zabicie terminala lub keyboardinterrupt
        if cv2.waitKey(1) & 0xFF == ord('q') or (cv2.getWindowProperty('motion detection', cv2.WND_PROP_VISIBLE) < 1):
            break

    video.release()
    if output is not None:
        output.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    detect_movement()
