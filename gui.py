import customtkinter
import tkinter
from PIL import Image
import cv2
import numpy as np
import HandTrackingModule as HM
import autopy
import autopy.mouse
import time


customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

root = customtkinter.CTk()
root.title("HGC")

window_width = 900
window_height = 550

root.resizable(False, False)

# Центриране на прозореца на екрана


def center_screen():
    global screen_height, screen_width, x_cordinate, y_cordinate

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_cordinate = int((screen_width/2) - (window_width/2))
    y_cordinate = int((screen_height/2) - (window_height/2))
    root.geometry("{}x{}+{}+{}".format(window_width,
                  window_height, x_cordinate, y_cordinate))

# старттиране на камерата


def camera_control():
    camera_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
    print("Стартиране")

    infolbl = customtkinter.CTkLabel(
        master=camera_frame, text="Изберете ръка с която да работите", font=('Calibri', 25))
    infolbl.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)

    def back_to_main():
        camera_frame.place_forget()
        camera_frame_right.place_forget()
        camera_frame_left.place_forget()
        menu_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    def rightHand_cv():  # Стартиране на приложението с контрол на дясната
        camera_frame_right.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        infolbl = customtkinter.CTkLabel(
            master=camera_frame_right, text="Не използвайте приложението докато камерата работи", font=('Calibri', 30))
        infolbl.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        root.iconify()

        cap = cv2.VideoCapture(0)
        detector = HM.handDetector(detectionCon=0.7)
        clicked = False
        delay = 0.5
        # ID та на върговете на пръсте:
        tipIds = [4, 8, 12, 16, 20]

        camWidth = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        camHeight = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        SCREEN_WIDTH, SCREEN_HEIGHT = autopy.screen.size()

        while True:
            success, img = cap.read()
            img = cv2.flip(img, 1)
            img = detector.findHands(img)
            lmList = detector.findPosition(img, draw=False)
            cv2.putText(img, "Exit Press ESC", (10, 450),
                        cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
            if lmList:
                # List за запвазване на вискчи пръсти
                fingers = [0, 0, 0, 0, 0]

                # Палец
                if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:
                    fingers[0] = 1

                # Прости от показалец до котре:
                for i in range(1, 5):
                    if lmList[tipIds[i]][2] < lmList[tipIds[i] - 2][2]:
                        fingers[i] = 1

                # Проверка за показалец и среден, дали са вдигнати:
                if fingers[1] == 1 and fingers[2] == 1 and fingers[0] == 0 and fingers[3] == 0 and fingers[4] == 0:
                    # ако проверкатра е изпълнена правилно, се вкючва конрола на мишката "Mouse Control"
                    cv2.putText(img, "Mouse Control", (10, 50),
                                cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
                    x1, y1 = lmList[8][1:]
                    x2, y2 = lmList[12][1:]

                    # Поцицията на мишката на екрана според показацела и средния пръст:
                    x = x1 * SCREEN_WIDTH / camWidth
                    y = y1 * SCREEN_HEIGHT / camHeight
                    y = y * 1.5
                    x = x * 1.5
                    if x < 0:
                        x = 0
                    elif x > SCREEN_WIDTH - 1:
                        x = SCREEN_WIDTH - 1
                    if y < 0:
                        y = 0
                    elif y > SCREEN_HEIGHT - 1:
                        y = SCREEN_HEIGHT - 1
                    autopy.mouse.move(x, y)
                    time.sleep(0.01)

                # Проверка за алец и показалец
                elif fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
                    cv2.putText(img, "Pinch", (10, 50),
                                cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

                # Проверка за показалец, среден и безимен
                elif fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 0:
                    cv2.putText(img, "Right-Click", (10, 50),
                                cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
                    autopy.mouse.click(autopy.mouse.Button.RIGHT)
                    time.sleep(delay)

                # Проверка за отворена ръка
                elif fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:
                    cv2.putText(img, "Hand is spread", (10, 50),
                                cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

                # Проверка за показалец
                elif fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
                    print("click")
                    if not clicked:
                        clicked = True
                        cv2.putText(img, "Click", (10, 50),
                                    cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
                        autopy.mouse.click()
                        time.sleep(delay)
                    else:
                        clicked = False

                # Проверка за свита ръка
                elif fingers[0] == 0 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
                    cv2.putText(img, "Fist", (10, 50),
                                cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
                    autopy.mouse.toggle(autopy.mouse.Button.LEFT, True)

                # Проверка за всички не регисрирани знаци
                else:
                    totalFingers = fingers.count(1)
                    cv2.putText(img, "Other gesture", (10, 50),
                                cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

            cv2.imshow("Image", img)
            if cv2.waitKey(5) & 0xFF == 27:
                break
        cap.release()
        cv2.destroyAllWindows()

    btn_back_main = customtkinter.CTkButton(master=camera_frame_right, text="Към главното меню", font=(
        'Calibri', 18), width=180, height=45, command=back_to_main)
    btn_back_main.place(relx=0.8, rely=0.85, anchor=tkinter.CENTER)

    def leftHand_cv():  # Стартиране на приложението с контрол на дясната
        camera_frame_left.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        infolbl = customtkinter.CTkLabel(
            master=camera_frame_left, text="Не използвайте приложението докато камерата работи", font=('Calibri', 30))
        infolbl.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        root.iconify()

        cap = cv2.VideoCapture(0)
        detector = HM.handDetector(detectionCon=0.7)

        clicked = False
        delay = 0.5
        # ID та на върговете на пръсте:
        tipIds = [4, 8, 12, 16, 20]

        camWidth = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        camHeight = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        SCREEN_WIDTH, SCREEN_HEIGHT = autopy.screen.size()

        while True:
            success, img = cap.read()
            img = detector.findHands(img)
            lmList = detector.findPosition(img, draw=False)
            cv2.putText(img, "Exit Press ESC", (10, 450),
                        cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

            if lmList:
                # List за запвазване на вискчи пръсти
                fingers = [0, 0, 0, 0, 0]

                # Палец
                if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:
                    fingers[0] = 1

                # Прости от показалец до котре:
                for i in range(1, 5):
                    if lmList[tipIds[i]][2] < lmList[tipIds[i] - 2][2]:
                        fingers[i] = 1

                # Проверка за показалец и среден, дали са вдигнати:
                prev_x, prev_y = 0, 0  # initialize previous position

                # check if the middle and index fingers are up and the other fingers are down
                if fingers[1] == 1 and fingers[2] == 1 and fingers[0] == 0 and fingers[3] == 0 and fingers[4] == 0:
                    # if the condition is met, enable mouse control
                    cv2.putText(img, "Mouse Control", (10, 50),
                                cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
                    x1, y1 = lmList[8][1:]
                    x2, y2 = lmList[12][1:]

                    # calculate the position of the mouse on the screen based on the index and middle fingers
                    x = x1 * SCREEN_WIDTH / camWidth
                    y = y1 * SCREEN_HEIGHT / camHeight
                    y = y * 1.5
                    x = SCREEN_WIDTH - x * 1.5  # reverse the x direction
                    if x < 0:
                        x = 0
                    elif x > SCREEN_WIDTH - 1:
                        x = SCREEN_WIDTH - 1
                    if y < 0:
                        y = 0
                    elif y > SCREEN_HEIGHT - 1:
                        y = SCREEN_HEIGHT - 1
                    autopy.mouse.move(x, y)
                    time.sleep(0.01)

                # Проверка за алец и показалец
                elif fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
                    cv2.putText(img, "Pinch", (10, 50),
                                cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

                # Проверка за показалец, среден и безимен
                elif fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 0:
                    cv2.putText(img, "Right-Click", (10, 50),
                                cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
                    autopy.mouse.click(autopy.mouse.Button.RIGHT)
                    time.sleep(delay)

                # Проверка за отворена ръка
                elif fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:
                    cv2.putText(img, "Hand is spread", (10, 50),
                                cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

                # Проверка за показалец
                elif fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
                    print("click")
                    if not clicked:
                        clicked = True
                        cv2.putText(img, "Click", (10, 50),
                                    cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
                        autopy.mouse.click()
                        time.sleep(delay)
                    else:
                        clicked = False

                # Проверка за свита ръка
                elif fingers[0] == 0 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
                    cv2.putText(img, "Fist", (10, 50),
                                cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
                    autopy.mouse.toggle(autopy.mouse.Button.LEFT, True)

                # Проверка за всички не регисрирани знаци
                else:
                    totalFingers = fingers.count(1)
                    cv2.putText(img, "Other gesture", (10, 50),
                                cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

            cv2.imshow("Image", img)
            if cv2.waitKey(5) & 0xFF == 27:
                break
        cap.release()
        cv2.destroyAllWindows()

        btn_back_main = customtkinter.CTkButton(master=camera_frame_left, text="Към главното меню", font=(
            'Calibri', 18), width=180, height=45, command=back_to_main)
        btn_back_main.place(relx=0.8, rely=0.85, anchor=tkinter.CENTER)

    rightHand = customtkinter.CTkButton(
        master=camera_frame, text="Дясна ръка", command=rightHand_cv)
    rightHand.place(relx=0.6, rely=0.5, anchor=tkinter.CENTER)

    leftHand = customtkinter.CTkButton(
        master=camera_frame, text="Лява ръка", command=leftHand_cv)
    leftHand.place(relx=0.4, rely=0.5, anchor=tkinter.CENTER)

    btn_back_main = customtkinter.CTkButton(master=use_frame, text="Към главното меню", font=(
        'Calibri', 18), width=180, height=45, command=back_to_main)
    btn_back_main.place(relx=0.8, rely=0.85, anchor=tkinter.CENTER)


# Как да използваме приложението
def how_to_use():

    def back_to_main_btn():
        use_frame.place_forget()
        use_frame2.place_forget()
        use_frame3.place_forget()
        use_frame4.place_forget()
        print("back")

    # как да използваме приложението стр.1
    use_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
    infolbl = customtkinter.CTkLabel(
        master=use_frame, text="Как да използваме приложението", font=('Calibri', 25))
    infolbl.place(relx=0.25, rely=0.1, anchor=tkinter.CENTER)

    movePointTxt = customtkinter.CTkTextbox(master=use_frame, width=350, height=250, font=(
        "", 16), fg_color="transparent", wrap="word")
    movePointTxt.place(relx=0.28, rely=0.55, anchor=tkinter.CENTER)
    movePointTxt.insert("0.0", "Управление на мишката: Когато приложението разпознае специфичен жест, например показалецът и средният пръст са изправени, то променя позицията на мишката върху екрана, като пресмята координатите спрямо положението на ръката в кадъра на уебкамерата. Това позволява на потребителя да движи мишката, като премества ръката си пред камерата.")

    movePointImg = customtkinter.CTkImage(light_image=Image.open(
        "D:\\uni\\Diploma\\img\\mouse_move.png"), size=(220, 220))
    imgplace = customtkinter.CTkLabel(use_frame, text="", image=movePointImg)
    imgplace.place(relx=0.7, rely=0.5, anchor=tkinter.CENTER)

    def next_page1():
        use_frame.place_forget()
        use_frame2.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        print("стр.2")

    nextbtn = customtkinter.CTkButton(
        master=use_frame, text="Напред", width=80, command=next_page1)
    nextbtn.place(relx=0.48, rely=0.85, anchor=tkinter.CENTER)

    btn_back_main = customtkinter.CTkButton(master=use_frame, text="Към главното меню", font=(
        'Calibri', 18), width=180, height=45, command=back_to_main_btn)
    btn_back_main.place(relx=0.8, rely=0.85, anchor=tkinter.CENTER)

    # как да използваме приложението стр.2

    infolbl = customtkinter.CTkLabel(
        master=use_frame2, text="Как да използваме приложението", font=('Calibri', 25))
    infolbl.place(relx=0.25, rely=0.1, anchor=tkinter.CENTER)

    movePointTxt = customtkinter.CTkTextbox(master=use_frame2, width=350, height=250, font=(
        "", 16), fg_color="transparent", wrap="word")
    movePointTxt.place(relx=0.28, rely=0.55, anchor=tkinter.CENTER)
    movePointTxt.insert("0.0", "Кликване на мишката: Приложението разпознава жеста на показалец, когато показалецът е изправен, но другите пръсти са сгънати. Тогава се изпълнява кликване на мишката, което може да служи за избор на обекти или бутони на екрана.")

    movePointImg = customtkinter.CTkImage(light_image=Image.open(
        "D:\\uni\\Diploma\\img\\click.png"), size=(220, 220))
    imgplace = customtkinter.CTkLabel(use_frame2, text="", image=movePointImg)
    imgplace.place(relx=0.7, rely=0.5, anchor=tkinter.CENTER)

    def next_page2():
        use_frame2.place_forget()
        use_frame3.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        print("стр.3")

    def back_page():
        use_frame2.place_forget()
        use_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        print("стр.1")

    nextbtn = customtkinter.CTkButton(
        master=use_frame2, text="Напред", width=80, command=next_page2)
    nextbtn.place(relx=0.5, rely=0.85, anchor=tkinter.CENTER)

    back_pagebtn = customtkinter.CTkButton(
        master=use_frame2, text="Назад", width=80, command=back_page)
    back_pagebtn.place(relx=0.4, rely=0.85, anchor=tkinter.CENTER)

    btn_back_main = customtkinter.CTkButton(master=use_frame2, text="Към главното меню", font=(
        'Calibri', 18), width=180, height=45, command=back_to_main_btn)
    btn_back_main.place(relx=0.8, rely=0.85, anchor=tkinter.CENTER)

    # как да използваме приложението стр.3

    infolbl = customtkinter.CTkLabel(
        master=use_frame3, text="Как да използваме приложението", font=('Calibri', 25))
    infolbl.place(relx=0.25, rely=0.1, anchor=tkinter.CENTER)

    movePointTxt = customtkinter.CTkTextbox(master=use_frame3, width=350, height=250, font=(
        "", 16), fg_color="transparent", wrap="word")
    movePointTxt.place(relx=0.28, rely=0.55, anchor=tkinter.CENTER)
    movePointTxt.insert("0.0", "Десен бутон на мишката: Когато показалецът, средният пръст и безименният пръст са изправени, приложението разпознава жеста за десен бутон на мишката. Това позволява на потребителя да извършва десен клик на мишката, който може да отваря контекстни менюта или изпълнява други команди, свързани с десния бутон.")

    movePointImg = customtkinter.CTkImage(light_image=Image.open(
        "D:\\uni\\Diploma\\img\\right_click.png"), size=(220, 220))
    imgplace = customtkinter.CTkLabel(use_frame3, text="", image=movePointImg)
    imgplace.place(relx=0.7, rely=0.5, anchor=tkinter.CENTER)

    def next_page3():
        use_frame3.place_forget()
        use_frame4.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        print("стр.4")

    def back_page2():
        use_frame3.place_forget()
        use_frame2.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        print("стр.2")

    nextbtn2 = customtkinter.CTkButton(
        master=use_frame3, text="Напред", width=80, command=next_page3)
    nextbtn2.place(relx=0.5, rely=0.85, anchor=tkinter.CENTER)

    back_pagebtn2 = customtkinter.CTkButton(
        master=use_frame3, text="Назад", width=80, command=back_page2)
    back_pagebtn2.place(relx=0.4, rely=0.85, anchor=tkinter.CENTER)

    btn_back_main = customtkinter.CTkButton(master=use_frame3, text="Към главното меню", font=(
        'Calibri', 18), width=180, height=45, command=back_to_main_btn)
    btn_back_main.place(relx=0.8, rely=0.85, anchor=tkinter.CENTER)

    # как да използваме приложението стр.4

    infolbl = customtkinter.CTkLabel(
        master=use_frame4, text="Как да използваме приложението", font=('Calibri', 25))
    infolbl.place(relx=0.25, rely=0.1, anchor=tkinter.CENTER)

    movePointTxt = customtkinter.CTkTextbox(master=use_frame4, width=350, height=250, font=(
        "", 16), fg_color="transparent", wrap="word")
    movePointTxt.place(relx=0.28, rely=0.55, anchor=tkinter.CENTER)
    movePointTxt.insert("0.0", "Сгъната ръка: Това може да се използва за извършване на действия, като например превъртане на екрана или избиране на опция в менюто чрез определени жестове на ръката, в зависимост от функционалността на приложението.")

    movePointImg = customtkinter.CTkImage(light_image=Image.open(
        "D:\\uni\\Diploma\\img\\fist.jpg"), size=(220, 220))
    imgplace = customtkinter.CTkLabel(use_frame4, text="", image=movePointImg)
    imgplace.place(relx=0.7, rely=0.5, anchor=tkinter.CENTER)

    def back_page3():
        use_frame4.place_forget()
        use_frame3.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    back_pagebtn3 = customtkinter.CTkButton(
        master=use_frame4, text="Назад", width=80, command=back_page3)
    back_pagebtn3.place(relx=0.48, rely=0.85, anchor=tkinter.CENTER)

    btn_back_main = customtkinter.CTkButton(master=use_frame4, text="Към главното меню", font=(
        'Calibri', 18), width=180, height=45, command=back_to_main_btn)
    btn_back_main.place(relx=0.8, rely=0.85, anchor=tkinter.CENTER)

    print("Как да използваме приложението")

# Информация за приложението


def info_app():
    info_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
    infoLbl = customtkinter.CTkLabel(
        master=info_frame, text="Информация за приложението", font=('Calibri', 25))
    infoLbl.place(relx=0.3, rely=0.15, anchor=tkinter.CENTER)
    aboutTxt = customtkinter.CTkTextbox(master=info_frame, wrap="word", width=680, height=290, font=(
        'Calobri', 18), fg_color="transparent")
    aboutTxt.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
    aboutTxt.insert("0.0", "Приложението е създадено за управление на компютър с помощта на жестове на ръката. То използва уебкамерата на компютъра, за да разпознава позициите на пръстите на ръката и да извършва определени действия в зависимост от жестовете.")
    aboutTxt.configure(state="disable")

    def back_to_main_btn():
        info_frame.place_forget()
        print("back")

    btn_back = customtkinter.CTkButton(master=info_frame, text="Към главното меню", font=(
        'Calibri', 18), width=180, height=45, command=back_to_main_btn)
    btn_back.place(relx=0.8, rely=0.85, anchor=tkinter.CENTER)
    print("Info about application")


# изход
def exit_app():
    root.destroy()
    print("Exit")


# Главно меню
menu_frame = customtkinter.CTkFrame(
    master=root, width=400, height=400, fg_color="transparent")
menu_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

main_menu_lbl = customtkinter.CTkLabel(
    master=menu_frame, text="Hand Gesture Control", font=('Century Gothic', 34))
main_menu_lbl.place(relx=0.5, rely=0.09, anchor=tkinter.CENTER)

cam_btn = customtkinter.CTkButton(master=menu_frame, text="Стартиране", font=(
    'Calibri', 18), width=180, height=45, command=camera_control)
cam_btn.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

how_btn = customtkinter.CTkButton(master=menu_frame, text="Ръководство", font=(
    'Calibri', 18), width=180, height=45, command=how_to_use)
how_btn.place(relx=0.5, rely=0.55, anchor=tkinter.CENTER)

info_btn = customtkinter.CTkButton(master=menu_frame, text="Информация", font=(
    'Calibri', 18), width=180, height=45, command=info_app)
info_btn.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

exit_btn = customtkinter.CTkButton(master=menu_frame, text="Изход", font=(
    'Calibri', 18), width=180, height=45, command=exit_app)
exit_btn.place(relx=0.5, rely=0.85, anchor=tkinter.CENTER)

# Фреймове за различните под менюта
info_frame = customtkinter.CTkFrame(
    master=root, width=900, height=550, fg_color="transparent")
use_frame = customtkinter.CTkFrame(
    master=root, width=900, height=550, fg_color="transparent")
camera_frame = customtkinter.CTkFrame(
    master=root, width=900, height=550, fg_color="transparent")


use_frame2 = customtkinter.CTkFrame(
    master=root, width=900, height=550, fg_color="transparent")
use_frame3 = customtkinter.CTkFrame(
    master=root, width=900, height=550, fg_color="transparent")
use_frame4 = customtkinter.CTkFrame(
    master=root, width=900, height=550, fg_color="transparent")
camera_frame_right = customtkinter.CTkFrame(
    master=root, width=900, height=550, fg_color="transparent")
camera_frame_left = customtkinter.CTkFrame(
    master=root, width=900, height=550, fg_color="transparent")
center_screen()
root.mainloop()
