# TextInput 3 character limit:
#       https://groups.google.com/g/kivy-users/c/xTcDcm2eKEE


from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
import time
import threading
import socket
from math import sqrt
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.properties import BooleanProperty
from kivy.clock import mainthread
from kivy.uix.popup import Popup
from kivy.config import Config

Config.set('input', 'mouse', 'mouse,multitouch_on_demand') # Disable multi touch
stop = False

green = [0/255, 176/255, 80/255, 1]
grey = [166/255, 166/255, 166/255, 1]

is_connected = False  # Check if it's connected.


class LimitInput(TextInput):
    valid_characters = "0123456789.,"

    def insert_text(self, substring, from_undo=False):      # Operates to write only Valid_Characters.
        if substring in self.valid_characters:
            s = ''.join(substring)
            return super().insert_text(s, from_undo=from_undo)
        else:
            pass

    def keyboard_on_key_up(self, keycode, text):    # Allows to only press backspace when character limit is reached.
        if text[1] == 'enter':
            Clock.schedule_once(AdvancedControlPage.percentage_init)
        if self.readonly and text[1] == "backspace":
            self.readonly = False
            self.do_backspace()


class Calc:
    @staticmethod
    def total_current(i_1, i_2, i_3, i_4, i_5, i_6):
        return i_1 + i_2 + i_3 + i_4 + i_5 + i_6

    @staticmethod
    def i_lineer_percentage(v, i_lineer, kva, pf):
        return (v * i_lineer) * 100 / (kva * pf * 1000)

    @staticmethod
    def i_nonlineer_percentage(v, i_nonlineer, kva, pf):
        return (v * i_nonlineer * 0.7) * 100 / (kva * pf * 1000)

    @staticmethod
    def kw_2(v, i_lineer, i_nonlineer):
        return v * (i_lineer + 0.7 * i_nonlineer)

    @staticmethod
    def power_factor2(kw_2, kva_2):
        return kw_2 / kva_2

    @staticmethod
    def kva_2(v, i_lineer, i_nonlineer):
        # # # print(f"v={v}, i_lineer={i_lineer}, i_nonlineer={i_nonlineer}")
        return sqrt((v * (i_lineer + (0.7 * i_nonlineer))) ** 2 + (v * 0.3 * 2.41 * i_nonlineer) ** 2)

    @staticmethod
    def kw_prc(kw_2, kva, pf):  # kW percentage (%kW)
        return kw_2 / (kva * pf * 1000)

    @staticmethod
    def kva_prc(kva_2, kva):  # kVA percentage (%kVA)
        return kva_2 / (kva * 1000)

    @staticmethod
    def percentage(v, kva, pf, i):

        i_lineer_total = Calc.total_current(i[0], i[1], i[2], i[3], i[4], i[5])
        i_nonlineer_total = Calc.total_current(i[6], i[7], i[8], i[9], i[10], 0)

        kw_2 = Calc.kw_2(v, i_lineer_total, i_nonlineer_total)
        kva_2 = Calc.kva_2(v, i_lineer_total, i_nonlineer_total)

        power_factor2 = Calc.power_factor2(kw_2, kva_2)

        kw_prc = Calc.kw_prc(kw_2, kva, pf)  # kW percentage (%kW)
        kva_prc = Calc.kva_prc(kva_2, kva)  # kVA percentage (%kVA)

        i1_prc = 0
        i2_prc = 0
        i3_prc = 0
        i4_prc = 0
        i5_prc = 0
        i6_prc = 0
        i7_prc = 0
        i8_prc = 0
        i9_prc = 0
        i10_prc = 0
        i11_prc = 0

        if kw_prc >= kva_prc:
            i1_prc = Calc.i_lineer_percentage(v, i[0], kva, pf)
            i2_prc = Calc.i_lineer_percentage(v, i[1], kva, pf)
            i3_prc = Calc.i_lineer_percentage(v, i[2], kva, pf)
            i4_prc = Calc.i_lineer_percentage(v, i[3], kva, pf)
            i5_prc = Calc.i_lineer_percentage(v, i[4], kva, pf)
            i6_prc = Calc.i_lineer_percentage(v, i[5], kva, pf)

            i7_prc = Calc.i_nonlineer_percentage(v, i[6], kva, pf)
            i8_prc = Calc.i_nonlineer_percentage(v, i[7], kva, pf)
            i9_prc = Calc.i_nonlineer_percentage(v, i[8], kva, pf)
            i10_prc = Calc.i_nonlineer_percentage(v, i[9], kva, pf)
            i11_prc = Calc.i_nonlineer_percentage(v, i[10], kva, pf)

        elif kva_prc > kw_prc:
            i1_prc = Calc.i_lineer_percentage(v, i[0], kva, power_factor2)
            i2_prc = Calc.i_lineer_percentage(v, i[1], kva, power_factor2)
            i3_prc = Calc.i_lineer_percentage(v, i[2], kva, power_factor2)
            i4_prc = Calc.i_lineer_percentage(v, i[3], kva, power_factor2)
            i5_prc = Calc.i_lineer_percentage(v, i[4], kva, power_factor2)
            i6_prc = Calc.i_lineer_percentage(v, i[5], kva, power_factor2)

            i7_prc = Calc.i_nonlineer_percentage(v, i[6], kva, power_factor2)
            i8_prc = Calc.i_nonlineer_percentage(v, i[7], kva, power_factor2)
            i9_prc = Calc.i_nonlineer_percentage(v, i[8], kva, power_factor2)
            i10_prc = Calc.i_nonlineer_percentage(v, i[9], kva, power_factor2)
            i11_prc = Calc.i_nonlineer_percentage(v, i[10], kva, power_factor2)
            pass

        return [kw_2, kva_2, power_factor2, kw_prc, kva_prc, round(i1_prc, 2), round(i2_prc, 2), round(i3_prc, 2),
                round(i4_prc, 2), round(i5_prc, 2), round(i6_prc, 2), round(i7_prc, 2), round(i8_prc, 2),
                round(i9_prc, 2), round(i10_prc, 2), round(i11_prc, 2)]


class PasswordPopUp(Popup):

    def test(self):
        if self.password.text == 'AsDq08333600':
            App.get_running_app().root.current = 'optionpage'
    pass


class BlankPage(Screen):
    app_started = False

    def on_enter(self, *args):
        Clock.schedule_once(self.testt, 0.01)  # Try to connect again.
        pass

    def testt(self, *args):
        a = open("ip.txt", "r").read().split('\n')  # Read .txt file
        if len(a) < 2:
            a.append('')
        if len(a) < 3:
            a.append('')
        if len(a) < 4:
            a.append('')
        if len(a) < 5:
            a.append('General')
        if a[4] == "Advanced":
            self.parent.current = 'advancedcontrolpage'

        elif a[4] == "General":
            self.parent.current = 'generalcontrolpage'
        a = "\n".join(a)
        f = open("ip.txt", "w")
        f.write(a)  # Save the file
        f.close()

    def get_start_screen(self, *args):
        pass

    def test(self):
        self.parent.current = 'generalcontrolpage'
    pass


class GeneralControlPage(Screen):
    r_loads = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]     # Temporary Status of buttons
    s_loads = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    t_loads = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    r_calc_loads = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]    # Final Status of buttons
    s_calc_loads = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    t_calc_loads = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    total_r_prc = 0
    total_s_prc = 0
    total_t_prc = 0

    thread_pause = BooleanProperty(False)
    is_connected = False  # Check if it's connected.
    is_setup_done = False  # Setup condition
    is_trying_to_connect = False
    brake_connection = False
    connection_check_flag = False
    block_calculation = False
    block_calculation_reset = False

    def all_on_button(self):
        if self.masteronof.background_color == grey:
            self.block_calculation = True
            Clock.schedule_once(self.all_on_calc, 0.15)

    def all_on_calc(self, *args):
        self.r_calc_loads = [1.5, 3, 6, 9, 18, 32, 0, 0, 0, 0, 0]
        self.r_loads = [1.5, 3, 6, 9, 18, 32, 0, 0, 0, 0, 0]
        self.s_calc_loads = [1.5, 3, 6, 9, 18, 32, 0, 0, 0, 0, 0]
        self.s_loads = [1.5, 3, 6, 9, 18, 32, 0, 0, 0, 0, 0]
        self.t_calc_loads = [1.5, 3, 6, 9, 18, 32, 0, 0, 0, 0, 0]
        self.t_loads = [1.5, 3, 6, 9, 18, 32, 0, 0, 0, 0, 0]
        self.calculation([1.5, 3, 6, 9, 18, 32, 0, 0, 0, 0, 0], "r")
        time.sleep(0.0001)
        self.calculation([1.5, 3, 6, 9, 18, 32, 0, 0, 0, 0, 0], "s")
        time.sleep(0.0001)
        self.calculation([1.5, 3, 6, 9, 18, 32, 0, 0, 0, 0, 0], "t")
        time.sleep(0.0001)
        self.block_calculation = False

    def reset_button(self):
        self.block_calculation = True
        self.block_calculation_reset = True
        Clock.schedule_once(self.reset_calc, 0.15)

    def reset_calc(self, *args):
        self.r_calc_loads = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.r_loads = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.s_calc_loads = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.s_loads = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.t_calc_loads = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.t_loads = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.calculation([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "r")
        time.sleep(0.0001)
        self.calculation([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "s")
        time.sleep(0.0001)
        self.calculation([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "t")
        time.sleep(0.0001)
        self.block_calculation = False
        self.block_calculation_reset = False

    def percentage_init(self, *args):
        try:
            # # print(threading.enumerate())
            if float(self.pf.text.replace(',', '.')) == 0:
                return
            initial_calculation = Calc.percentage(float(self.v.text), float(self.kva.text),
                                                  float(self.pf.text.replace(',', '.')),
                                                  [1.5, 3, 6, 9, 18, 32, 0, 0, 0, 0, 0])
            # Edit spesific line
            a = open("ip.txt", "r").read().split('\n')  # Read .txt file
            a[1] = self.v.text  # Write to a spesific line
            a[2] = self.kva.text  # Write to a spesific line
            a[3] = self.pf.text  # Write to a spesific line
            a = "\n".join(a)
            f = open("ip.txt", "w")
            f.write(a)  # Save the file
            f.close()
            if initial_calculation[3] >= initial_calculation[4]:
                self.r_1.text = f' 1,5A\n%{initial_calculation[5]}'
                self.r_2.text = f' 3A\n%{initial_calculation[6]}'
                self.r_3.text = f' 6A\n%{initial_calculation[7]}'
                self.r_4.text = f' 9A\n%{initial_calculation[8]}'
                self.r_5.text = f' 18A\n%{initial_calculation[9]}'
                self.r_6.text = f' 32A\n%{initial_calculation[10]}'

                self.s_1.text = f' 1,5A\n%{initial_calculation[5]}'
                self.s_2.text = f' 3A\n%{initial_calculation[6]}'
                self.s_3.text = f' 6A\n%{initial_calculation[7]}'
                self.s_4.text = f' 9A\n%{initial_calculation[8]}'
                self.s_5.text = f' 18A\n%{initial_calculation[9]}'
                self.s_6.text = f' 32A\n%{initial_calculation[10]}'

                self.t_1.text = f' 1,5A\n%{initial_calculation[5]}'
                self.t_2.text = f' 3A\n%{initial_calculation[6]}'
                self.t_3.text = f' 6A\n%{initial_calculation[7]}'
                self.t_4.text = f' 9A\n%{initial_calculation[8]}'
                self.t_5.text = f' 18A\n%{initial_calculation[9]}'
                self.t_6.text = f' 32A\n%{initial_calculation[10]}'

            if self.r_loads[0:5] != [0, 0, 0, 0, 0]:
                r_prc_enter = Calc.percentage(float(self.v.text), float(self.kva.text),
                                              float(self.pf.text.replace(',', '.')), self.r_calc_loads)
                total_r_prc = 0
                if r_prc_enter[4] > r_prc_enter[3]:
                    self.r_1.text = f" 1,5A\n%{r_prc_enter[5]}" if r_prc_enter[5] != 0 else "1,5A"
                    self.r_2.text = f" 3A\n%{r_prc_enter[6]}" if r_prc_enter[6] != 0 else "3A"
                    self.r_3.text = f" 6A\n%{r_prc_enter[7]}" if r_prc_enter[7] != 0 else "6A"
                    self.r_4.text = f" 9A\n%{r_prc_enter[8]}" if r_prc_enter[8] != 0 else "9A"
                    self.r_5.text = f" 18A\n%{r_prc_enter[9]}" if r_prc_enter[9] != 0 else "18A"
                    self.r_6.text = f" 32A\n%{r_prc_enter[10]}" if r_prc_enter[10] != 0 else "32A"
                for k in range(5, 16):
                    total_r_prc = total_r_prc + r_prc_enter[k]
                # print(total_r_prc, r_prc_enter)
                self.r_prc1.text = f"%{round(total_r_prc, 2)}" if self.block_calculation_reset is False else "%0"

            if self.s_loads[0:5] != [0, 0, 0, 0, 0]:
                s_prc_enter = Calc.percentage(float(self.v.text), float(self.kva.text),
                                              float(self.pf.text.replace(',', '.')), self.s_calc_loads)
                total_s_prc = 0
                # # # print(s_prc_enter)
                if s_prc_enter[4] > s_prc_enter[3]:
                    # # # print("testtt")
                    self.s_1.text = f" 1,5A\n%{s_prc_enter[5]}" if s_prc_enter[5] != 0 else "1,5A"
                    self.s_2.text = f" 3A\n%{s_prc_enter[6]}" if s_prc_enter[6] != 0 else "3A"
                    self.s_3.text = f" 6A\n%{s_prc_enter[7]}" if s_prc_enter[7] != 0 else "6A"
                    self.s_4.text = f" 9A\n%{s_prc_enter[8]}" if s_prc_enter[8] != 0 else "9A"
                    self.s_5.text = f" 18A\n%{s_prc_enter[9]}" if s_prc_enter[9] != 0 else "18A"
                    self.s_6.text = f" 32A\n%{s_prc_enter[10]}" if s_prc_enter[10] != 0 else "32A"
                    self.s_7.text = f" 4A\n%{s_prc_enter[11]}" if s_prc_enter[11] != 0 else "4A"
                    self.s_8.text = f" 8A\n%{s_prc_enter[12]}" if s_prc_enter[12] != 0 else "8A"
                    self.s_9.text = f" 15A\n%{s_prc_enter[13]}" if s_prc_enter[13] != 0 else "15A"
                    self.s_10.text = f" 22A\n%{s_prc_enter[14]}" if s_prc_enter[14] != 0 else "22A"
                    self.s_11.text = f" 42A\n%{s_prc_enter[15]}" if s_prc_enter[15] != 0 else "42A"
                for k in range(5, 16):
                    total_s_prc = total_s_prc + s_prc_enter[k]
                self.s_prc1.text = f"%{round(total_s_prc, 2)}" if self.block_calculation_reset is False else "%0"

            if self.t_loads[0:5] != [0, 0, 0, 0, 0]:
                # # # print("t_loads =", self.t_loads)
                # # # print("t_calc_loads =", self.t_calc_loads)
                t_prc_enter = Calc.percentage(float(self.v.text), float(self.kva.text),
                                              float(self.pf.text.replace(',', '.')), self.t_calc_loads)
                total_t_prc = 0
                if t_prc_enter[4] > t_prc_enter[3]:
                    self.t_1.text = f" 1,5A\n%{t_prc_enter[5]}" if t_prc_enter[5] != 0 else "1,5A"
                    self.t_2.text = f" 3A\n%{t_prc_enter[6]}" if t_prc_enter[6] != 0 else "3A"
                    self.t_3.text = f" 6A\n%{t_prc_enter[7]}" if t_prc_enter[7] != 0 else "6A"
                    self.t_4.text = f" 9A\n%{t_prc_enter[8]}" if t_prc_enter[8] != 0 else "9A"
                    self.t_5.text = f" 18A\n%{t_prc_enter[9]}" if t_prc_enter[9] != 0 else "18A"
                    self.t_6.text = f" 32A\n%{t_prc_enter[10]}" if t_prc_enter[10] != 0 else "32A"
                    self.t_7.text = f" 4A\n%{t_prc_enter[11]}" if t_prc_enter[11] != 0 else "4A"
                    self.t_8.text = f" 8A\n%{t_prc_enter[12]}" if t_prc_enter[12] != 0 else "8A"
                    self.t_9.text = f" 15A\n%{t_prc_enter[13]}" if t_prc_enter[13] != 0 else "15A"
                    self.t_10.text = f" 22A\n%{t_prc_enter[14]}" if t_prc_enter[14] != 0 else "22A"
                    self.t_11.text = f" 42A\n%{t_prc_enter[15]}" if t_prc_enter[15] != 0 else "42A"
                for k in range(5, 16):
                    total_t_prc = total_t_prc + t_prc_enter[k]
                self.t_prc1.text = f"%{round(total_t_prc, 2)}" if self.block_calculation_reset is False else "%0"
        except ValueError as e:
            self.v.text = ''
            self.kva.text = ''
            self.pf.text = ''
            # # print("Wrong Input", e)

    def calculation(self, loads, phase):
        try:
            prc_calculation = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # Stores

            if phase == "r":
                if loads != [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]:
                    if self.v.text != '' and self.kva.text != '' and self.pf.text != '':
                        prc_calculation = Calc.percentage(float(self.v.text), float(self.kva.text),
                                                          float(self.pf.text.replace(',', '.')), loads)
                elif loads == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]:
                    prc_calculation = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                total_r_prc = 0
                for k in range(5, 16):
                    total_r_prc = total_r_prc + prc_calculation[k]
                if prc_calculation[4] > prc_calculation[3]:
                    self.r_1.text = f" 1,5A\n%{prc_calculation[5]}" if prc_calculation[5] != 0 else "1,5A"
                    self.r_2.text = f" 3A\n%{prc_calculation[6]}" if prc_calculation[6] != 0 else "3A"
                    self.r_3.text = f" 6A\n%{prc_calculation[7]}" if prc_calculation[7] != 0 else "6A"
                    self.r_4.text = f" 9A\n%{prc_calculation[8]}" if prc_calculation[8] != 0 else "9A"
                    self.r_5.text = f" 18A\n%{prc_calculation[9]}" if prc_calculation[9] != 0 else "18A"
                    self.r_6.text = f" 32A\n%{prc_calculation[10]}" if prc_calculation[10] != 0 else "32A"

                elif prc_calculation[3] >= prc_calculation[4]:
                    self.percentage_init()
                    self.r_1.text = self.r_1.text if prc_calculation[11] == 0 else "1,5A"
                    self.r_2.text = self.r_2.text if prc_calculation[12] == 0 else "3A"
                    self.r_3.text = self.r_3.text if prc_calculation[13] == 0 else "6A"
                    self.r_4.text = self.r_4.text if prc_calculation[14] == 0 else "9A"
                    self.r_5.text = self.r_5.text if prc_calculation[15] == 0 else "18A"

                self.r_prc1.text = f"%{round(total_r_prc, 2)}"

            elif phase == "s":
                if loads != [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]:
                    if self.v.text != '' and self.kva.text != '' and self.pf.text != '':
                        prc_calculation = Calc.percentage(float(self.v.text), float(self.kva.text),
                                                          float(self.pf.text.replace(',', '.')), loads)
                elif loads == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]:
                    prc_calculation = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                total_s_prc = 0
                for k in range(5, 16):
                    total_s_prc = total_s_prc + prc_calculation[k]
                if prc_calculation[4] > prc_calculation[3]:
                    self.s_1.text = f" 1,5A\n%{prc_calculation[5]}" if prc_calculation[5] != 0 else "1,5A"
                    self.s_2.text = f" 3A\n%{prc_calculation[6]}" if prc_calculation[6] != 0 else "3A"
                    self.s_3.text = f" 6A\n%{prc_calculation[7]}" if prc_calculation[7] != 0 else "6A"
                    self.s_4.text = f" 9A\n%{prc_calculation[8]}" if prc_calculation[8] != 0 else "9A"
                    self.s_5.text = f" 18A\n%{prc_calculation[9]}" if prc_calculation[9] != 0 else "18A"
                    self.s_6.text = f" 32A\n%{prc_calculation[10]}" if prc_calculation[10] != 0 else "32A"
                elif prc_calculation[3] >= prc_calculation[4]:
                    self.percentage_init()
                    self.s_1.text = self.s_1.text if prc_calculation[11] == 0 else "1,5A"
                    self.s_2.text = self.s_2.text if prc_calculation[12] == 0 else "3A"
                    self.s_3.text = self.s_3.text if prc_calculation[13] == 0 else "6A"
                    self.s_4.text = self.s_4.text if prc_calculation[14] == 0 else "9A"
                    self.s_5.text = self.s_5.text if prc_calculation[15] == 0 else "18A"
                self.s_prc1.text = f"%{round(total_s_prc, 2)}"

            elif phase == "t":
                if loads != [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]:
                    if self.v.text != '' and self.kva.text != '' and self.pf.text != '':
                        prc_calculation = Calc.percentage(float(self.v.text), float(self.kva.text),
                                                          float(self.pf.text.replace(',', '.')), loads)
                elif loads == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]:
                    prc_calculation = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                total_t_prc = 0
                for k in range(5, 16):
                    total_t_prc = total_t_prc + prc_calculation[k]
                if prc_calculation[4] > prc_calculation[3]:
                    self.t_1.text = f" 1,5A\n%{prc_calculation[5]}" if prc_calculation[5] != 0 else "1,5A"
                    self.t_2.text = f" 3A\n%{prc_calculation[6]}" if prc_calculation[6] != 0 else "3A"
                    self.t_3.text = f" 6A\n%{prc_calculation[7]}" if prc_calculation[7] != 0 else "6A"
                    self.t_4.text = f" 9A\n%{prc_calculation[8]}" if prc_calculation[8] != 0 else "9A"
                    self.t_5.text = f" 18A\n%{prc_calculation[9]}" if prc_calculation[9] != 0 else "18A"
                    self.t_6.text = f" 32A\n%{prc_calculation[10]}" if prc_calculation[10] != 0 else "32A"
                elif prc_calculation[3] >= prc_calculation[4]:
                    self.percentage_init()
                    self.t_1.text = self.t_1.text if prc_calculation[11] == 0 else "1,5A"
                    self.t_2.text = self.t_2.text if prc_calculation[12] == 0 else "3A"
                    self.t_3.text = self.t_3.text if prc_calculation[13] == 0 else "6A"
                    self.t_4.text = self.t_4.text if prc_calculation[14] == 0 else "9A"
                    self.t_5.text = self.t_5.text if prc_calculation[15] == 0 else "18A"
                self.t_prc1.text = f"%{round(total_t_prc, 2)}"
        except ValueError as e:
            self.v.text = ''
            self.kva.text = ''
            self.pf.text = ''
            # # print("Wrong Input", e)
            pass

    def on_enter(self, *args):
        self.brake_connection = False
        self.thread_pause = False

        if self.is_setup_done is False:  # Setting thread and clock for once.
            self.is_setup_done = True
            Clock.schedule_once(self.getip, 0.01)  # At the start, get IP from txt file
            Clock.schedule_once(self.tcp_thread_start, 0.01)  # Start tcp thread
            if self.connection_check_flag is False:
                Clock.schedule_interval(self.connection_check, 0.5)  # Check connection if its still on going.
                self.connection_check_flag = True

    def on_pre_leave(self, *args):
        self.brake_connection = True
        self.is_setup_done = False

    @mainthread
    def getip(self, *args):
        # Edit spesific line
        a = open("ip.txt", "r").read().split('\n')  # Read .txt file
        self.v.text = a[1]
        self.kva.text = a[2]
        self.pf.text = a[3]
        self.box.text = open("ip.txt", "r").read().split('\n')[0]

    @mainthread
    def tick(self, *args):
        self.status.source = "tick.png"
        self.status3.source = "tick.png"

    @mainthread
    def cross(self, *args):
        self.status.source = "cross.png"
        self.status3.source = "cross.png"

    def tcp_thread_start(self, *args):
        y = threading.Thread(target=self.tcp_thread, daemon=False)  # Setup thread
        y.start()  # Starts thread
        # # # print("testthreadstart", threading.enumerate())

    def tcp_thread(self):
        global s

        func = [self.r_onof, self.s_onof, self.t_onof,
                self.r_1, self.r_2, self.r_3, self.r_4, self.r_5, self.r_6, self.r_7, self.r_8, self.r_9,
                self.r_10, self.r_11,
                self.s_1, self.s_2, self.s_3, self.s_4, self.s_5, self.s_6, self.s_7, self.s_8, self.s_9,
                self.s_10, self.s_11,
                self.t_1, self.t_2, self.t_3, self.t_4, self.t_5, self.t_6, self.t_7, self.t_8, self.t_9,
                self.t_10, self.t_11, self.masteronof]

        var = [b'281010', b'291010', b'521010', b'531010', b'761010', b'771010', b'301010', b'311010', b'321010',
               b'331010', b'341010', b'351010', b'361010', b'371010', b'381010', b'391010', b'401010', b'411010',
               b'421010', b'431010', b'441010', b'451010', b'461010', b'471010', b'481010', b'491010', b'501010',
               b'511010', b'541010', b'551010', b'561010', b'571010', b'581010', b'591010', b'601010', b'611010',
               b'621010', b'631010', b'641010', b'651010', b'661010', b'671010', b'681010', b'691010', b'701010',
               b'711010', b'721010', b'731010', b'741010', b'751010', b'781010', b'791010', b'801010', b'811010',
               b'821010', b'831010', b'841010', b'851010', b'861010', b'871010', b'881010', b'891010', b'901010',
               b'911010', b'921010', b'931010', b'941010', b'951010', b'961010', b'971010', b'981010', b'991010']

        varr = ["q", "Q", "f", "F", "n", "N", "w", "W", "e", "E", "r", "R", "t", "T", "y", "Y", "u", "U", "o", "O",
                "p", "P", "a", "A", "s", "S", "d", "D", "g", "G", "h", "H", "j", "J", "k", "K", "l", "L", "i", "I",
                "z", "Z", "x", "X", "c", "C", "v", "V", "b", "B", "m", "M", "1", "!", "2", "'", "3", "^", "4", "+",
                "5", "%", "6", "&", "7", "/", "8", "(", "9", ")", "0", "=", "{", "}"]

        currents = [1.5, 3, 6, 9, 18, 32, 4, 8, 15, 22, 42]

        try:
            host = self.box.text  # Get IP from TextInput.
            port = 10001
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, port))  # Try to connect
                self.is_connected = True
                # If connected:
                self.is_trying_to_connect = False
                Clock.schedule_once(self.tick)  # Make Connection status ON (Green tick)

                # Edit spesific line
                a = open("ip.txt", "r").read().split('\n')  # Read .txt file
                a[0] = self.box.text  # Write to first line
                a = "\n".join(a)
                f = open("ip.txt", "w")
                f.write(a)  # Save the file
                f.close()

                s.sendall(bytes("|", 'ascii'))  # Send button's status.
                while True:
                    data = s.recv(1)  # Receive data
                    datastr = data.decode("utf-8")
                    # # # print("data has come")
                    # # # print(datastr, "general")

                    if self.brake_connection is True:
                        # # print("general control connection broke.")
                        self.thread_pause = True
                        break

                    previous_bg_color = []
                    for x in range(3, 36):  # Button states
                        previous_bg_color.append(func[x].background_color.copy())

                    for x in range(0, 74):
                        if varr[x] in datastr:  # Button state
                            if (x % 2) == 0:
                                func[int(x / 2)].background_color = [0/255, 176/255, 80/255, 1]  # Button State - ON
                                if x == 0 or x == 2 or x == 4 or x == 72:
                                    func[int(x / 2)].background_color = [146/255, 208/255, 80/255, 1]  # Button State - ON

                            elif (x % 2) == 1:
                                func[int((x - 1) / 2)].background_color = [166/255, 166/255, 166/255, 1]  # Button State - OFF

                    if self.block_calculation is False:
                        for x in range(3, 36):  # Changed Button States
                            # # print(x, "--->", func[x].background_color, previous_bg_color[x - 3])
                            if func[x].background_color != previous_bg_color[x - 3]:  # If button state is changed,
                                if func[x].background_color == [0/255, 176/255, 80/255, 1]:  # Button is ON

                                    if 3 <= x <= 13:  # R Phase
                                        self.r_loads[x - 3] = currents[x - 3]
                                        self.r_calc_loads = self.r_loads.copy()

                                        for i in range(0, 11):
                                            if 0 <= i <= 4:
                                                if self.r_loads[i] == 0:
                                                    self.r_calc_loads[i + 6] = 0

                                            if 6 <= i <= 10:
                                                if self.r_loads[i - 6] == 0:
                                                    self.r_calc_loads[i] = 0

                                                if self.r_loads[i] != 0:
                                                    self.r_calc_loads[i - 6] = 0
                                        self.calculation(self.r_calc_loads, "r")

                                    if 14 <= x <= 24:  # S Phase
                                        self.s_loads[x - 14] = currents[x - 14]
                                        self.s_calc_loads = self.s_loads.copy()

                                        for i in range(0, 11):
                                            if 0 <= i <= 4:
                                                if self.s_loads[i] == 0:
                                                    self.s_calc_loads[i + 6] = 0

                                            if 6 <= i <= 10:
                                                if self.s_loads[i - 6] == 0:
                                                    self.s_calc_loads[i] = 0

                                                if self.s_loads[i] != 0:
                                                    self.s_calc_loads[i - 6] = 0
                                        self.calculation(self.s_calc_loads, "s")

                                    if 25 <= x <= 35:  # T Phase
                                        self.t_loads[x - 25] = currents[x - 25]
                                        self.t_calc_loads = self.t_loads.copy()

                                        for i in range(0, 11):
                                            if 0 <= i <= 4:
                                                if self.t_loads[i] == 0:
                                                    self.t_calc_loads[i + 6] = 0

                                            if 6 <= i <= 10:
                                                if self.t_loads[i - 6] == 0:
                                                    self.t_calc_loads[i] = 0

                                                if self.t_loads[i] != 0:
                                                    self.t_calc_loads[i - 6] = 0
                                        self.calculation(self.t_calc_loads, "t")

                                if func[x].background_color == [166/255, 166/255, 166/255, 1]:  # Button is OFF
                                    if 3 <= x <= 13:  # R Phase
                                        self.r_loads[x - 3] = 0
                                        self.r_calc_loads = self.r_loads.copy()

                                        for i in range(0, 11):
                                            if 0 <= i <= 4:
                                                if self.r_loads[i] == 0:
                                                    self.r_calc_loads[i + 6] = 0

                                            if 6 <= i <= 10:
                                                if self.r_loads[i - 6] == 0:
                                                    self.r_calc_loads[i] = 0

                                                if self.r_loads[i] != 0:
                                                    self.r_calc_loads[i - 6] = 0
                                        self.calculation(self.r_calc_loads, "r")

                                    if 14 <= x <= 24:  # S Phase
                                        self.s_loads[x - 14] = 0
                                        self.s_calc_loads = self.s_loads.copy()

                                        for i in range(0, 11):
                                            if 0 <= i <= 4:
                                                if self.s_loads[i] == 0:
                                                    self.s_calc_loads[i + 6] = 0

                                            if 6 <= i <= 10:
                                                if self.s_loads[i - 6] == 0:
                                                    self.s_calc_loads[i] = 0

                                                if self.s_loads[i] != 0:
                                                    self.s_calc_loads[i - 6] = 0
                                        self.calculation(self.s_calc_loads, "s")

                                    if 25 <= x <= 35:  # T Phase
                                        self.t_loads[x - 25] = 0
                                        self.t_calc_loads = self.t_loads.copy()

                                        for i in range(0, 11):
                                            if 0 <= i <= 4:
                                                if self.t_loads[i] == 0:
                                                    self.t_calc_loads[i + 6] = 0

                                            if 6 <= i <= 10:
                                                if self.t_loads[i - 6] == 0:
                                                    self.t_calc_loads[i] = 0

                                                if self.t_loads[i] != 0:
                                                    self.t_calc_loads[i - 6] = 0
                                        self.calculation(self.t_calc_loads, "t")

                    if self.is_connected is False or data == ' ':  # If connection lost:
                        # # print("Connection lost.", self.is_connected)
                        break
            Clock.schedule_once(self.cross)  # Make Connection status OFF (Red cross)
            if self.thread_pause is False:
                Clock.schedule_once(self.tcp_thread_start, 0.01)  # Try to connect again.

        except Exception as e:  # If it couldn't connect
            self.is_connected = False
            self.is_trying_to_connect = True
            # # print(self.thread_pause)
            if self.thread_pause is False:
                Clock.schedule_once(self.tcp_thread_start, 0.01)  # Try to connect again.
            Clock.schedule_once(self.cross)  # Make Connection status OFF (Red cross)
            # # print("generalcontrol crash", e)

    @mainthread
    def test(self):
        pass
        # # print(self.v.text)
        # # print("test Kivy Func inside TCP func")

    def send(self, x):
        try:
            if self.is_connected is True:
                s.sendall(bytes(x, 'ascii'))  # Send button's status.

        except Exception as e:  # If connection has lost:
            self.is_connected = False
            self.status3.source = "cross.png"  # Make Connection status OFF (Red cross)
            # # print("fail,", e)

    def master_onof(self, x):
        try:
            if x is False:  # If Master button is OFF
                s.sendall(bytes("q", 'ascii'))  # Make all on/off buttons ON.
                s.sendall(bytes("f", 'ascii'))  # Make all on/off buttons ON.
                s.sendall(bytes("n", 'ascii'))  # Make all on/off buttons ON.
            elif x is True:  # If Master button is ON
                s.sendall(bytes("Q", 'ascii'))  # Make all on/off buttons OFF.
                s.sendall(bytes("F", 'ascii'))  # Make all on/off buttons OFF.
                s.sendall(bytes("N", 'ascii'))  # Make all on/off buttons OFF.
        except Exception as e:  # If connection has lost:
            self.is_connected = False
            self.status3.source = "cross.png"  # Make Connection status OFF (Red cross)
            # # print("fail,", e)

    def connection_check(self, dt):
        global s

        try:
            if self.is_connected is False:
                pass
            elif self.is_connected is True:
                s.sendall(b'\x11')  # Sending a byte to check if connection is lost.
                self.is_connected = True  # Connection is on going.
                time.sleep(0.05)

        except:
            self.is_connected = False  # Connection is lost.
            # # print(f"Connection is lost, is_connected = {self.is_connected}")


class AdvancedControlPage(Screen):
    r_loads = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # Temporary Status of buttons
    s_loads = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    t_loads = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    r_calc_loads = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # Final Status of buttons
    s_calc_loads = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    t_calc_loads = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    total_r_prc = 0
    total_s_prc = 0
    total_t_prc = 0

    thread_pause = BooleanProperty(False)
    is_connected = False  # Check if it's connected.
    is_setup_done = False  # Setup condition
    is_trying_to_connect = False
    brake_connection = False
    connection_check_flag = False
    block_calculation = False
    block_calculation_reset = False

    def reset(self):
        reset_chars = ["Q", "F", "N", "W", "E", "R", "T", "Y", "U", "O", "P", "A", "S", "D", "G", "H", "J", "K", "L",
                       "I", "Z", "X", "C", "V", "B", "M", "!", "'", "^", "+", "%", "&", "/", "(", ")", "=", "}"]
        for i in range(0, 37):
            s.sendall(bytes(reset_chars[i], 'ascii'))

    def all_on(self):
        reset_chars = ["w", "e", "r", "t", "y", "u", "o", "p", "a", "s", "d", "g", "h", "j", "k", "l",
                       "i", "z", "x", "c", "v", "b", "m", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "{"]
        for i in range(0, 37):
            s.sendall(bytes(reset_chars[i], 'ascii'))

    def all_on_button(self):
        if self.masteronof.background_color == grey:
            self.block_calculation = True
            Clock.schedule_once(self.all_on_calc, 0.15)

    def all_on_calc(self, *args):

        self.r_calc_loads = [0, 0, 0, 0, 0, 32, 4, 8, 15, 22, 42]
        self.r_loads = [1.5, 3, 6, 9, 18, 32, 4, 8, 15, 22, 42]

        self.s_calc_loads = [0, 0, 0, 0, 0, 32, 4, 8, 15, 22, 42]
        self.s_loads = [1.5, 3, 6, 9, 18, 32, 4, 8, 15, 22, 42]

        self.t_calc_loads = [0, 0, 0, 0, 0, 32, 4, 8, 15, 22, 42]
        self.t_loads = [1.5, 3, 6, 9, 18, 32, 4, 8, 15, 22, 42]

        self.calculation([0, 0, 0, 0, 0, 32, 4, 8, 15, 22, 42], "r")
        time.sleep(0.0001)
        self.calculation([0, 0, 0, 0, 0, 32, 4, 8, 15, 22, 42], "s")
        time.sleep(0.0001)
        self.calculation([0, 0, 0, 0, 0, 32, 4, 8, 15, 22, 42], "t")
        self.calculation([0, 0, 0, 0, 0, 32, 4, 8, 15, 22, 42], "r")
        time.sleep(0.0001)
        self.block_calculation = False
        # print(self.r_calc_loads, "r_calc")

    def reset_button(self):
        self.block_calculation = True
        self.block_calculation_reset = True
        Clock.schedule_once(self.reset_calc, 0.15)

    def reset_calc(self, *args):
        self.r_calc_loads = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.r_loads = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.s_calc_loads = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.s_loads = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.t_calc_loads = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.t_loads = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.calculation([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "r")
        time.sleep(0.0001)
        self.calculation([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "s")
        time.sleep(0.0001)
        self.calculation([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "t")
        time.sleep(0.0001)
        self.block_calculation = False
        self.block_calculation_reset = False

    def percentage_init(self, *args):
        # print("init works")
        try:
            if float(self.pf.text.replace(',', '.')) == 0:
                return
            initial_calculation = Calc.percentage(float(self.v.text), float(self.kva.text),
                                                  float(self.pf.text.replace(',', '.')),
                                                  [1.5, 3, 6, 9, 18, 32, 0, 0, 0, 0, 0])
            # Edit spesific line
            a = open("ip.txt", "r").read().split('\n')  # Read .txt file
            a[1] = self.v.text  # Save to ip.txt
            a[2] = self.kva.text  # Save to ip.txt
            a[3] = self.pf.text  # Save to ip.txt
            a = "\n".join(a)
            f = open("ip.txt", "w")
            f.write(a)  # Save the file
            f.close()

            if initial_calculation[3] >= initial_calculation[4]:
                self.r_1.text = f' 1,5A\n%{initial_calculation[5]}'
                self.r_2.text = f' 3A\n%{initial_calculation[6]}'
                self.r_3.text = f' 6A\n%{initial_calculation[7]}'
                self.r_4.text = f' 9A\n%{initial_calculation[8]}'
                self.r_5.text = f' 18A\n%{initial_calculation[9]}'
                self.r_6.text = f' 32A\n%{initial_calculation[10]}'

                self.s_1.text = f' 1,5A\n%{initial_calculation[5]}'
                self.s_2.text = f' 3A\n%{initial_calculation[6]}'
                self.s_3.text = f' 6A\n%{initial_calculation[7]}'
                self.s_4.text = f' 9A\n%{initial_calculation[8]}'
                self.s_5.text = f' 18A\n%{initial_calculation[9]}'
                self.s_6.text = f' 32A\n%{initial_calculation[10]}'

                self.t_1.text = f' 1,5A\n%{initial_calculation[5]}'
                self.t_2.text = f' 3A\n%{initial_calculation[6]}'
                self.t_3.text = f' 6A\n%{initial_calculation[7]}'
                self.t_4.text = f' 9A\n%{initial_calculation[8]}'
                self.t_5.text = f' 18A\n%{initial_calculation[9]}'
                self.t_6.text = f' 32A\n%{initial_calculation[10]}'

            if self.r_loads[0:5] != [0, 0, 0, 0, 0]:
                r_prc_enter = Calc.percentage(float(self.v.text), float(self.kva.text),
                                              float(self.pf.text.replace(',', '.')), self.r_calc_loads)
                total_r_prc = 0
                if r_prc_enter[4] > r_prc_enter[3]:
                    # # # print("flagflag19", r_prc_enter)
                    # # # print(r_prc_enter[5], r_prc_enter[6], r_prc_enter[15])
                    self.r_1.text = f" 1,5A\n%{r_prc_enter[5]}" if r_prc_enter[5] != 0 else "1,5A"
                    self.r_2.text = f" 3A\n%{r_prc_enter[6]}" if r_prc_enter[6] != 0 else "3A"
                    self.r_3.text = f" 6A\n%{r_prc_enter[7]}" if r_prc_enter[7] != 0 else "6A"
                    self.r_4.text = f" 9A\n%{r_prc_enter[8]}" if r_prc_enter[8] != 0 else "9A"
                    self.r_5.text = f" 18A\n%{r_prc_enter[9]}" if r_prc_enter[9] != 0 else "18A"
                    self.r_6.text = f" 32A\n%{r_prc_enter[10]}" if r_prc_enter[10] != 0 else "32A"
                for k in range(5, 16):
                    total_r_prc = total_r_prc + r_prc_enter[k]
                self.r_prc2.text = f"%{round(total_r_prc, 2)}" if self.block_calculation_reset is False else "%0"

            if self.s_loads[0:5] != [0, 0, 0, 0, 0]:
                s_prc_enter = Calc.percentage(float(self.v.text), float(self.kva.text),
                                              float(self.pf.text.replace(',', '.')), self.s_calc_loads)
                total_s_prc = 0
                # # # print(s_prc_enter)
                if s_prc_enter[4] > s_prc_enter[3]:
                    # # # print("testtt")
                    self.s_1.text = f" 1,5A\n%{s_prc_enter[5]}" if s_prc_enter[5] != 0 else "1,5A"
                    self.s_2.text = f" 3A\n%{s_prc_enter[6]}" if s_prc_enter[6] != 0 else "3A"
                    self.s_3.text = f" 6A\n%{s_prc_enter[7]}" if s_prc_enter[7] != 0 else "6A"
                    self.s_4.text = f" 9A\n%{s_prc_enter[8]}" if s_prc_enter[8] != 0 else "9A"
                    self.s_5.text = f" 18A\n%{s_prc_enter[9]}" if s_prc_enter[9] != 0 else "18A"
                    self.s_6.text = f" 32A\n%{s_prc_enter[10]}" if s_prc_enter[10] != 0 else "32A"
                    self.s_7.text = f" 4A\n%{s_prc_enter[11]}" if s_prc_enter[11] != 0 else "4A"
                    self.s_8.text = f" 8A\n%{s_prc_enter[12]}" if s_prc_enter[12] != 0 else "8A"
                    self.s_9.text = f" 15A\n%{s_prc_enter[13]}" if s_prc_enter[13] != 0 else "15A"
                    self.s_10.text = f" 22A\n%{s_prc_enter[14]}" if s_prc_enter[14] != 0 else "22A"
                    self.s_11.text = f" 42A\n%{s_prc_enter[15]}" if s_prc_enter[15] != 0 else "42A"
                for k in range(5, 16):
                    total_s_prc = total_s_prc + s_prc_enter[k]
                self.s_prc2.text = f"%{round(total_s_prc, 2)}" if self.block_calculation_reset is False else "%0"

            if self.t_loads[0:5] != [0, 0, 0, 0, 0]:
                # # # print("t_loads =", self.t_loads)
                # # # print("t_calc_loads =", self.t_calc_loads)
                t_prc_enter = Calc.percentage(float(self.v.text), float(self.kva.text),
                                              float(self.pf.text.replace(',', '.')), self.t_calc_loads)
                total_t_prc = 0
                if t_prc_enter[4] > t_prc_enter[3]:
                    self.t_1.text = f" 1,5A\n%{t_prc_enter[5]}" if t_prc_enter[5] != 0 else "1,5A"
                    self.t_2.text = f" 3A\n%{t_prc_enter[6]}" if t_prc_enter[6] != 0 else "3A"
                    self.t_3.text = f" 6A\n%{t_prc_enter[7]}" if t_prc_enter[7] != 0 else "6A"
                    self.t_4.text = f" 9A\n%{t_prc_enter[8]}" if t_prc_enter[8] != 0 else "9A"
                    self.t_5.text = f" 18A\n%{t_prc_enter[9]}" if t_prc_enter[9] != 0 else "18A"
                    self.t_6.text = f" 32A\n%{t_prc_enter[10]}" if t_prc_enter[10] != 0 else "32A"
                    self.t_7.text = f" 4A\n%{t_prc_enter[11]}" if t_prc_enter[11] != 0 else "4A"
                    self.t_8.text = f" 8A\n%{t_prc_enter[12]}" if t_prc_enter[12] != 0 else "8A"
                    self.t_9.text = f" 15A\n%{t_prc_enter[13]}" if t_prc_enter[13] != 0 else "15A"
                    self.t_10.text = f" 22A\n%{t_prc_enter[14]}" if t_prc_enter[14] != 0 else "22A"
                    self.t_11.text = f" 42A\n%{t_prc_enter[15]}" if t_prc_enter[15] != 0 else "42A"
                for k in range(5, 16):
                    total_t_prc = total_t_prc + t_prc_enter[k]
                self.t_prc2.text = f"%{round(total_t_prc, 2)}" if self.block_calculation_reset is False else "%0"

        except ValueError as e:
            self.v.text = ''
            self.kva.text = ''
            self.pf.text = ''
            # # print("Wrong Input", e)

    def calculation(self, loads, phase, *args):
        try:
            prc_calculation = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # Stores

            if phase == "r":
                r_phase_init = Calc.percentage(float(self.v.text), float(self.kva.text),
                                               float(self.pf.text.replace(',', '.')),
                                               [1.5, 3, 6, 9, 18, 32, 0, 0, 0, 0, 0])
                if loads != [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]:
                    if self.v.text != '' and self.kva.text != '' and self.pf.text != '':
                        prc_calculation = Calc.percentage(float(self.v.text), float(self.kva.text),
                                                          float(self.pf.text.replace(',', '.')), loads)
                        # print(prc_calculation)

                elif loads == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]:
                    prc_calculation = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                total_r_prc = 0

                for k in range(5, 16):
                    total_r_prc = total_r_prc + prc_calculation[k]

                if prc_calculation[4] > prc_calculation[3]:
                    self.r_1.text = f" 1,5A\n%{prc_calculation[5]}" if prc_calculation[5] != 0 else "1,5A"
                    self.r_2.text = f" 3A\n%{prc_calculation[6]}" if prc_calculation[6] != 0 else "3A"
                    self.r_3.text = f" 6A\n%{prc_calculation[7]}" if prc_calculation[7] != 0 else "6A"
                    self.r_4.text = f" 9A\n%{prc_calculation[8]}" if prc_calculation[8] != 0 else "9A"
                    self.r_5.text = f" 18A\n%{prc_calculation[9]}" if prc_calculation[9] != 0 else "18A"
                    self.r_6.text = f" 32A\n%{prc_calculation[10]}" if prc_calculation[10] != 0 else "32A"
                    self.r_7.text = f" 4A\n%{prc_calculation[11]}" if prc_calculation[11] != 0 else "4A"
                    self.r_8.text = f" 8A\n%{prc_calculation[12]}" if prc_calculation[12] != 0 else "8A"
                    self.r_9.text = f" 15A\n%{prc_calculation[13]}" if prc_calculation[13] != 0 else "15A"
                    self.r_10.text = f" 22A\n%{prc_calculation[14]}" if prc_calculation[14] != 0 else "22A"
                    self.r_11.text = f" 42A\n%{prc_calculation[15]}" if prc_calculation[15] != 0 else "42A"

                elif prc_calculation[3] >= prc_calculation[4]:

                    self.r_1.text = f" 1,5A\n%{r_phase_init[5]}"
                    self.r_2.text = f" 3A\n%{r_phase_init[6]}"
                    self.r_3.text = f" 6A\n%{r_phase_init[7]}"
                    self.r_4.text = f" 9A\n%{r_phase_init[8]}"
                    self.r_5.text = f" 12A\n%{r_phase_init[9]}"
                    self.r_6.text = f" 42A\n%{r_phase_init[10]}"

                    if self.r_1.background_color == grey:     # 1,5A is OFF
                        self.r_7.text = "4A"
                    else:
                        if self.r_7.background_color == grey:    # 4A is OFF
                            self.r_1.text = f" 1,5A\n%{prc_calculation[5]}"
                            self.r_7.text = "4A"
                        else:
                            self.r_1.text = "1,5A"
                            self.r_7.text = f' 4A\n%{prc_calculation[11]}'

                    if self.r_2.background_color == grey:  # 3A is OFF
                        self.r_8.text = "8A"
                    else:
                        if self.r_8.background_color == grey:  # 8A is OFF
                            self.r_2.text = f" 3A\n%{prc_calculation[6]}"
                            self.r_8.text = "8A"
                        else:
                            self.r_2.text = "3A"
                            self.r_8.text = f' 8A\n%{prc_calculation[12]}'

                    if self.r_3.background_color == grey:     # 6A is OFF
                        self.r_9.text = "15A"
                    else:
                        if self.r_9.background_color == grey:    # 15A is OFF
                            self.r_3.text = f" 6A\n%{prc_calculation[7]}"
                            self.r_9.text = "15A"
                        else:
                            self.r_3.text = "6A"
                            self.r_9.text = f' 15A\n%{prc_calculation[13]}'

                    if self.r_4.background_color == grey:     # 9A is OFF
                        self.r_10.text = "22A"
                    else:
                        if self.r_10.background_color == grey:    # 22A is OFF
                            self.r_4.text = f" 9A\n%{prc_calculation[8]}"
                            self.r_10.text = "22A"
                        else:
                            self.r_4.text = "9A"
                            self.r_10.text = f' 22A\n%{prc_calculation[14]}'

                    if self.r_5.background_color == grey:     # 12A is OFF
                        self.r_11.text = "42A"
                    else:
                        if self.r_11.background_color == grey:    # 42A is OFF
                            self.r_5.text = f" 12A\n%{prc_calculation[9]}"
                            self.r_11.text = "42A"
                        else:
                            self.r_5.text = "12A"
                            self.r_11.text = f' 42A\n%{prc_calculation[15]}'

                self.r_prc2.text = f"%{round(total_r_prc, 2)}"

            elif phase == "s":
                s_phase_init = Calc.percentage(float(self.v.text), float(self.kva.text),
                                               float(self.pf.text.replace(',', '.')),
                                               [1.5, 3, 6, 9, 18, 32, 0, 0, 0, 0, 0])
                if loads != [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]:
                    if self.v.text != '' and self.kva.text != '' and self.pf.text != '':
                        prc_calculation = Calc.percentage(float(self.v.text), float(self.kva.text),
                                                          float(self.pf.text.replace(',', '.')), loads)
                elif loads == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]:
                    prc_calculation = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                total_s_prc = 0
                for k in range(5, 16):
                    total_s_prc = total_s_prc + prc_calculation[k]
                if prc_calculation[4] > prc_calculation[3]:
                    self.s_1.text = f" 1,5A\n%{prc_calculation[5]}" if prc_calculation[5] != 0 else "1,5A"
                    self.s_2.text = f" 3A\n%{prc_calculation[6]}" if prc_calculation[6] != 0 else "3A"
                    self.s_3.text = f" 6A\n%{prc_calculation[7]}" if prc_calculation[7] != 0 else "6A"
                    self.s_4.text = f" 9A\n%{prc_calculation[8]}" if prc_calculation[8] != 0 else "9A"
                    self.s_5.text = f" 18A\n%{prc_calculation[9]}" if prc_calculation[9] != 0 else "18A"
                    self.s_6.text = f" 32A\n%{prc_calculation[10]}" if prc_calculation[10] != 0 else "32A"
                    self.s_7.text = f" 4A\n%{prc_calculation[11]}" if prc_calculation[11] != 0 else "4A"
                    self.s_8.text = f" 8A\n%{prc_calculation[12]}" if prc_calculation[12] != 0 else "8A"
                    self.s_9.text = f" 15A\n%{prc_calculation[13]}" if prc_calculation[13] != 0 else "15A"
                    self.s_10.text = f" 22A\n%{prc_calculation[14]}" if prc_calculation[14] != 0 else "22A"
                    self.s_11.text = f" 42A\n%{prc_calculation[15]}" if prc_calculation[15] != 0 else "42A"

                elif prc_calculation[3] >= prc_calculation[4]:
                    self.s_1.text = f" 1,5A\n%{s_phase_init[5]}"
                    self.s_2.text = f" 3A\n%{s_phase_init[6]}"
                    self.s_3.text = f" 6A\n%{s_phase_init[7]}"
                    self.s_4.text = f" 9A\n%{s_phase_init[8]}"
                    self.s_5.text = f" 12A\n%{s_phase_init[9]}"
                    self.s_6.text = f" 42A\n%{s_phase_init[10]}"

                    if self.s_1.background_color == grey:  # 1,5A is OFF
                        self.s_7.text = "4A"
                    else:
                        if self.s_7.background_color == grey:  # 4A is OFF
                            self.s_1.text = f" 1,5A\n%{prc_calculation[5]}"
                            self.s_7.text = "4A"
                        else:
                            self.s_1.text = "1,5A"
                            self.s_7.text = f' 4A\n%{prc_calculation[11]}'

                    if self.s_2.background_color == grey:  # 3A is OFF
                        self.s_8.text = "8A"
                    else:
                        if self.s_8.background_color == grey:  # 8A is OFF
                            self.s_2.text = f" 3A\n%{prc_calculation[6]}"
                            self.s_8.text = "8A"
                        else:
                            self.s_2.text = "3A"
                            self.s_8.text = f' 8A\n%{prc_calculation[12]}'

                    if self.s_3.background_color == grey:  # 6A is OFF
                        self.s_9.text = "15A"
                    else:
                        if self.s_9.background_color == grey:  # 15A is OFF
                            self.s_3.text = f" 6A\n%{prc_calculation[7]}"
                            self.s_9.text = "15A"
                        else:
                            self.s_3.text = "6A"
                            self.s_9.text = f' 15A\n%{prc_calculation[13]}'

                    if self.s_4.background_color == grey:  # 9A is OFF
                        self.s_10.text = "22A"
                    else:
                        if self.s_10.background_color == grey:  # 22A is OFF
                            self.s_4.text = f" 9A\n%{prc_calculation[8]}"
                            self.s_10.text = "22A"
                        else:
                            self.s_4.text = "9A"
                            self.s_10.text = f' 22A\n%{prc_calculation[14]}'

                    if self.s_5.background_color == grey:  # 12A is OFF
                        self.s_11.text = "42A"
                    else:
                        if self.s_11.background_color == grey:  # 42A is OFF
                            self.s_5.text = f" 12A\n%{prc_calculation[9]}"
                            self.s_11.text = "42A"
                        else:
                            self.s_5.text = "12A"
                            self.s_11.text = f' 42A\n%{prc_calculation[15]}'
                self.s_prc2.text = f"%{round(total_s_prc, 2)}"

            elif phase == "t":
                t_phase_init = Calc.percentage(float(self.v.text), float(self.kva.text),
                                               float(self.pf.text.replace(',', '.')),
                                               [1.5, 3, 6, 9, 18, 32, 0, 0, 0, 0, 0])
                if loads != [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]:
                    if self.v.text != '' and self.kva.text != '' and self.pf.text != '':
                        prc_calculation = Calc.percentage(float(self.v.text), float(self.kva.text),
                                                          float(self.pf.text.replace(',', '.')), loads)
                        # # print(prc_calculation)
                elif loads == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]:
                    prc_calculation = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                total_t_prc = 0
                for k in range(5, 16):
                    total_t_prc = total_t_prc + prc_calculation[k]
                if prc_calculation[4] > prc_calculation[3]:
                    self.t_1.text = f" 1,5A\n%{prc_calculation[5]}" if prc_calculation[5] != 0 else "1,5A"
                    self.t_2.text = f" 3A\n%{prc_calculation[6]}" if prc_calculation[6] != 0 else "3A"
                    self.t_3.text = f" 6A\n%{prc_calculation[7]}" if prc_calculation[7] != 0 else "6A"
                    self.t_4.text = f" 9A\n%{prc_calculation[8]}" if prc_calculation[8] != 0 else "9A"
                    self.t_5.text = f" 18A\n%{prc_calculation[9]}" if prc_calculation[9] != 0 else "18A"
                    self.t_6.text = f" 32A\n%{prc_calculation[10]}" if prc_calculation[10] != 0 else "32A"
                    self.t_7.text = f" 4A\n%{prc_calculation[11]}" if prc_calculation[11] != 0 else "4A"
                    self.t_8.text = f" 8A\n%{prc_calculation[12]}" if prc_calculation[12] != 0 else "8A"
                    self.t_9.text = f" 15A\n%{prc_calculation[13]}" if prc_calculation[13] != 0 else "15A"
                    self.t_10.text = f" 22A\n%{prc_calculation[14]}" if prc_calculation[14] != 0 else "22A"
                    self.t_11.text = f" 42A\n%{prc_calculation[15]}" if prc_calculation[15] != 0 else "42A"

                elif prc_calculation[3] >= prc_calculation[4]:
                    self.t_1.text = f" 1,5A\n%{t_phase_init[5]}"
                    self.t_2.text = f" 3A\n%{t_phase_init[6]}"
                    self.t_3.text = f" 6A\n%{t_phase_init[7]}"
                    self.t_4.text = f" 9A\n%{t_phase_init[8]}"
                    self.t_5.text = f" 12A\n%{t_phase_init[9]}"
                    self.t_6.text = f" 42A\n%{t_phase_init[10]}"

                    if self.t_1.background_color == grey:  # 1,5A is OFF
                        self.t_7.text = "4A"
                    else:
                        if self.t_7.background_color == grey:  # 4A is OFF
                            self.t_1.text = f" 1,5A\n%{prc_calculation[5]}"
                            self.t_7.text = "4A"
                        else:
                            self.t_1.text = "1,5A"
                            self.t_7.text = f' 4A\n%{prc_calculation[11]}'

                    if self.t_2.background_color == grey:  # 3A is OFF
                        self.t_8.text = "8A"
                    else:
                        if self.t_8.background_color == grey:  # 8A is OFF
                            self.t_2.text = f" 3A\n%{prc_calculation[6]}"
                            self.t_8.text = "8A"
                        else:
                            self.t_2.text = "3A"
                            self.t_8.text = f' 8A\n%{prc_calculation[12]}'

                    if self.t_3.background_color == grey:  # 6A is OFF
                        self.t_9.text = "15A"
                    else:
                        if self.t_9.background_color == grey:  # 15A is OFF
                            self.t_3.text = f" 6A\n%{prc_calculation[7]}"
                            self.t_9.text = "15A"
                        else:
                            self.t_3.text = "6A"
                            self.t_9.text = f' 15A\n%{prc_calculation[13]}'

                    if self.t_4.background_color == grey:  # 9A is OFF
                        self.t_10.text = "22A"
                    else:
                        if self.t_10.background_color == grey:  # 22A is OFF
                            self.t_4.text = f" 9A\n%{prc_calculation[8]}"
                            self.t_10.text = "22A"
                        else:
                            self.t_4.text = "9A"
                            self.t_10.text = f' 22A\n%{prc_calculation[14]}'

                    if self.t_5.background_color == grey:  # 12A is OFF
                        self.t_11.text = "42A"
                    else:
                        if self.t_11.background_color == grey:  # 42A is OFF
                            self.t_5.text = f" 12A\n%{prc_calculation[9]}"
                            self.t_11.text = "42A"
                        else:
                            self.t_5.text = "12A"
                            self.t_11.text = f' 42A\n%{prc_calculation[15]}'
                self.t_prc2.text = f"%{round(total_t_prc, 2)}"

        except ValueError as e:
            self.v.text = ''
            self.kva.text = ''
            self.pf.text = ''
            # # print("Wrong Input", e)
            pass

    def on_enter(self, *args):
        self.brake_connection = False
        self.thread_pause = False

        if self.is_setup_done is False:  # Setting thread and clock for once.
            self.is_setup_done = True
            Clock.schedule_once(self.getip, 0.01)  # At the start, get IP from txt file
            Clock.schedule_once(self.tcp_thread_start, 0.01)  # Start tcp thread
            Clock.schedule_interval(self.connection_check, 0.5)  # Check connection if its still on going.
            if self.connection_check_flag is False:
                Clock.schedule_interval(self.connection_check, 0.5)  # Check connection if its still on going.
                self.connection_check_flag = True

    def on_pre_leave(self, *args):
        self.brake_connection = True
        self.is_setup_done = False

    @mainthread
    def getip(self, *args):
        # Edit spesific line
        a = open("ip.txt", "r").read().split('\n')  # Read .txt file
        self.v.text = a[1]
        self.kva.text = a[2]
        self.pf.text = a[3]
        self.box.text = open("ip.txt", "r").read().split('\n')[0]

    @mainthread
    def tick(self, *args):
        self.status.source = "tick.png"
        self.status2.source = "tick.png"

    @mainthread
    def cross(self, *args):
        self.status.source = "cross.png"
        self.status2.source = "cross.png"

    def tcp_thread_start(self, *args):
        y = threading.Thread(target=self.tcp_thread, daemon=False)  # Setup thread
        y.start()  # Starts thread
        # # # print("testthreadstart", threading.enumerate())

    def tcp_thread(self):
        global s

        func = [self.r_onof, self.s_onof, self.t_onof,
                self.r_1, self.r_2, self.r_3, self.r_4, self.r_5, self.r_6, self.r_7, self.r_8, self.r_9,
                self.r_10, self.r_11,
                self.s_1, self.s_2, self.s_3, self.s_4, self.s_5, self.s_6, self.s_7, self.s_8, self.s_9,
                self.s_10, self.s_11,
                self.t_1, self.t_2, self.t_3, self.t_4, self.t_5, self.t_6, self.t_7, self.t_8, self.t_9,
                self.t_10, self.t_11, self.masteronof]

        var = [b'281010', b'291010', b'521010', b'531010', b'761010', b'771010', b'301010', b'311010', b'321010',
               b'331010', b'341010', b'351010', b'361010', b'371010', b'381010', b'391010', b'401010', b'411010',
               b'421010', b'431010', b'441010', b'451010', b'461010', b'471010', b'481010', b'491010', b'501010',
               b'511010', b'541010', b'551010', b'561010', b'571010', b'581010', b'591010', b'601010', b'611010',
               b'621010', b'631010', b'641010', b'651010', b'661010', b'671010', b'681010', b'691010', b'701010',
               b'711010', b'721010', b'731010', b'741010', b'751010', b'781010', b'791010', b'801010', b'811010',
               b'821010', b'831010', b'841010', b'851010', b'861010', b'871010', b'881010', b'891010', b'901010',
               b'911010', b'921010', b'931010', b'941010', b'951010', b'961010', b'971010', b'981010', b'991010']

        varr = ["q", "Q", "f", "F", "n", "N", "w", "W", "e", "E", "r", "R", "t", "T", "y", "Y", "u", "U", "o", "O",
                "p", "P", "a", "A", "s", "S", "d", "D", "g", "G", "h", "H", "j", "J", "k", "K", "l", "L", "i", "I",
                "z", "Z", "x", "X", "c", "C", "v", "V", "b", "B", "m", "M", "1", "!", "2", "'", "3", "^", "4", "+",
                "5", "%", "6", "&", "7", "/", "8", "(", "9", ")", "0", "=", "{", "}"]

        currents = [1.5, 3, 6, 9, 18, 32, 4, 8, 15, 22, 42]

        try:
            host = self.box.text  # Get IP from TextInput.
            port = 10001
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, port))  # Try to connect
                self.is_connected = True
                # If connected:
                self.is_trying_to_connect = False
                Clock.schedule_once(self.tick)  # Make Connection status ON (Green tick)

                # Edit spesific line
                a = open("ip.txt", "r").read().split('\n')  # Read .txt file
                a[0] = self.box.text  # Write to first line
                a = "\n".join(a)
                f = open("ip.txt", "w")
                f.write(a)  # Save the file
                f.close()
                while True:
                    data = s.recv(2)  # Receive data
                    datastr = data.decode("utf-8")

                    # # print(datastr)

                    if self.brake_connection is True:
                        # # print("general control connection broke.")
                        self.thread_pause = True
                        break

                    previous_bg_color = []
                    for x in range(3, 36):  # Button states
                        previous_bg_color.append(func[x].background_color.copy())

                    for x in range(0, 74):
                        if varr[x] in datastr:  # Button state
                            if (x % 2) == 0:
                                func[int(x / 2)].background_color = [0/255, 176/255, 80/255, 1]  # Button State - ON
                                if x == 0 or x == 2 or x == 4 or x == 72:
                                    func[int(x / 2)].background_color = [146/255, 208/255, 80/255, 1]  # Button State - ON
                            elif (x % 2) == 1:
                                func[int((x - 1) / 2)].background_color = [166/255, 166/255, 166/255, 1]  # Button State-OFF

                    if self.block_calculation is False:
                        for x in range(3, 36):  # Changed Button States
                            if func[x].background_color != previous_bg_color[x - 3]:  # If button state is changed,
                                if func[x].background_color == [0/255, 176/255, 80/255, 1]:  # Button is ON

                                    if 3 <= x <= 13:  # R Phase
                                        self.r_loads[x - 3] = currents[x - 3]
                                        self.r_calc_loads = self.r_loads.copy()

                                        for i in range(0, 11):
                                            if 0 <= i <= 4:
                                                if self.r_loads[i] == 0:
                                                    self.r_calc_loads[i + 6] = 0

                                            if 6 <= i <= 10:
                                                if self.r_loads[i - 6] == 0:    # If Non-Lineer is ON,
                                                    self.r_calc_loads[i] = 0    # then Lineer won’t be calculated.

                                                if self.r_loads[i] != 0:
                                                    self.r_calc_loads[i - 6] = 0
                                        self.calculation(self.r_calc_loads, "r")

                                    if 14 <= x <= 24:  # S Phase
                                        self.s_loads[x - 14] = currents[x - 14]
                                        self.s_calc_loads = self.s_loads.copy()

                                        for i in range(0, 11):
                                            if 0 <= i <= 4:
                                                if self.s_loads[i] == 0:
                                                    self.s_calc_loads[i + 6] = 0

                                            if 6 <= i <= 10:
                                                if self.s_loads[i - 6] == 0:
                                                    self.s_calc_loads[i] = 0

                                                if self.s_loads[i] != 0:
                                                    self.s_calc_loads[i - 6] = 0
                                        self.calculation(self.s_calc_loads, "s")

                                    if 25 <= x <= 35:  # T Phase
                                        self.t_loads[x - 25] = currents[x - 25]
                                        self.t_calc_loads = self.t_loads.copy()

                                        for i in range(0, 11):
                                            if 0 <= i <= 4:
                                                if self.t_loads[i] == 0:
                                                    self.t_calc_loads[i + 6] = 0

                                            if 6 <= i <= 10:
                                                if self.t_loads[i - 6] == 0:
                                                    self.t_calc_loads[i] = 0

                                                if self.t_loads[i] != 0:
                                                    self.t_calc_loads[i - 6] = 0
                                        self.calculation(self.t_calc_loads, "t")

                                if func[x].background_color == [166/255, 166/255, 166/255, 1]:  # Button is OFF
                                    if 3 <= x <= 13:  # R Phase
                                        self.r_loads[x - 3] = 0
                                        self.r_calc_loads = self.r_loads.copy()

                                        for i in range(0, 11):
                                            if 0 <= i <= 4:
                                                if self.r_loads[i] == 0:
                                                    self.r_calc_loads[i + 6] = 0

                                            if 6 <= i <= 10:
                                                if self.r_loads[i - 6] == 0:
                                                    self.r_calc_loads[i] = 0

                                                if self.r_loads[i] != 0:
                                                    self.r_calc_loads[i - 6] = 0
                                        self.calculation(self.r_calc_loads, "r")

                                    if 14 <= x <= 24:  # S Phase
                                        self.s_loads[x - 14] = 0
                                        self.s_calc_loads = self.s_loads.copy()

                                        for i in range(0, 11):
                                            if 0 <= i <= 4:
                                                if self.s_loads[i] == 0:
                                                    self.s_calc_loads[i + 6] = 0

                                            if 6 <= i <= 10:
                                                if self.s_loads[i - 6] == 0:
                                                    self.s_calc_loads[i] = 0

                                                if self.s_loads[i] != 0:
                                                    self.s_calc_loads[i - 6] = 0
                                        self.calculation(self.s_calc_loads, "s")

                                    if 25 <= x <= 35:  # T Phase
                                        self.t_loads[x - 25] = 0
                                        self.t_calc_loads = self.t_loads.copy()

                                        for i in range(0, 11):
                                            if 0 <= i <= 4:
                                                if self.t_loads[i] == 0:
                                                    self.t_calc_loads[i + 6] = 0

                                            if 6 <= i <= 10:
                                                if self.t_loads[i - 6] == 0:
                                                    self.t_calc_loads[i] = 0

                                                if self.t_loads[i] != 0:
                                                    self.t_calc_loads[i - 6] = 0
                                        self.calculation(self.t_calc_loads, "t")


                    if self.is_connected is False or data == ' ':  # If connection lost:
                        # # print("Connection lost.", self.is_connected)
                        break
            Clock.schedule_once(self.cross)  # Make Connection status OFF (Red cross)
            if self.thread_pause is False:
                Clock.schedule_once(self.tcp_thread_start, 0.01)  # Try to connect again.

        except Exception as e:  # If it couldn't connect
            self.is_connected = False
            self.is_trying_to_connect = True
            # # print(self.thread_pause)
            if self.thread_pause is False:
                Clock.schedule_once(self.tcp_thread_start, 0.01)  # Try to connect again.
            Clock.schedule_once(self.cross)  # Make Connection status OFF (Red cross)
            # print("generalcontrol crash", e)

    def send(self, x):
        try:
            if self.is_connected is True:
                s.sendall(bytes(x, 'ascii'))  # Send button's status.

        except Exception as e:  # If connection has lost:
            self.is_connected = False
            self.status2.source = "cross.png"  # Make Connection status OFF (Red cross)
            # # print("fail,", e)

    def master_onof(self, x):
        try:
            if x is False:  # If Master button is OFF
                s.sendall(bytes("q", 'ascii'))  # Make all on/off buttons ON.
                s.sendall(bytes("f", 'ascii'))  # Make all on/off buttons ON.
                s.sendall(bytes("n", 'ascii'))  # Make all on/off buttons ON.
            elif x is True:  # If Master button is ON
                s.sendall(bytes("Q", 'ascii'))  # Make all on/off buttons OFF.
                s.sendall(bytes("F", 'ascii'))  # Make all on/off buttons OFF.
                s.sendall(bytes("N", 'ascii'))  # Make all on/off buttons OFF.
        except Exception as e:  # If connection has lost:
            self.is_connected = False
            self.status2.source = "cross.png"  # Make Connection status OFF (Red cross)
            # # print("fail,", e)

    def connection_check(self, dt):
        global s

        try:
            if self.is_connected is False:
                pass
            elif self.is_connected is True:
                s.sendall(b'\x11')  # Sending a byte to check if connection is lost.
                self.is_connected = True  # Connection is on going.
                time.sleep(0.05)

        except:
            self.is_connected = False  # Connection is lost.
            # # print(f"Connection is lost, is_connected = {self.is_connected}")

    def test(self):
        # # print("test")
        self.t_10.background_color = [0/255, 176/255, 80/255, 1]


class OptionPage(Screen):
    event = 0

    def on_enter(self, *args):
        a = open("ip.txt", "r").read().split('\n')  # Read .txt file
        self.box.text = a[0]
        if a[4] == "Advanced":
            self.checkbox_advanced.active = True
        if a[4] == "General":
            self.checkbox_general.active = True

    def save_ip(self):
        # Edit spesific line
        a = open("ip.txt", "r").read().split('\n')  # Read .txt file
        a[0] = self.box.text  # Write to first line
        a = "\n".join(a)
        f = open("ip.txt", "w")
        f.write(a)  # Save the file
        f.close()

    def pagestatus(self, status):
        a = open("ip.txt", "r").read().split('\n')  # Read .txt file
        if status == "Advanced":
            a[4] = "Advanced"
            a = "\n".join(a)
            f = open("ip.txt", "w")
            f.write(a)  # Save the file
            f.close()
        elif status == "General":
            a[4] = "General"
            a = "\n".join(a)
            f = open("ip.txt", "w")
            f.write(a)  # Save the file
            f.close()

    def back(self):
        # # print("screen changed")
        a = open("ip.txt", "r").read().split('\n')  # Read .txt file
        if a[4] == "Advanced":
            self.parent.current = 'advancedcontrolpage'
            # # print("CHANGED TO ADVANCED")

        elif a[4] == "General":
            self.parent.current = 'generalcontrolpage'
            # # print("CHANGED TO GENERAL")

    def thread_number(self):
        # # print(threading.enumerate())
        pass

    def disable_non_lineer(self, *args):
        try:
            s.sendall(bytes("|", 'ascii'))
            Clock.unschedule(self.event)
        except Exception as e:
            # # print(e)
            pass
    pass


class MainApp(App):

    def build(self):
        self.title = 'Röle Kontrol ESP32'
    Window.minimum_height = 540
    Window.minimum_width = 960
    Window.size = (1200, 675)

    def on_stop(self):
        global s
        s.close()

if __name__ == '__main__':
    MainApp().run()
