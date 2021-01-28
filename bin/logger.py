"""
File:                       ULTI02.py

Library Call Demonstrated:  mcculw.ul.t_in_scan()

Purpose:                    Scans temperature input channels.

Demonstration:              Displays the temperature inputs on a
                            range of channels.

Special Requirements:       Unless the board at BoardNum(=0) does not use
                            EXP boards for temperature measurements(the
                            CIO-DAS-TC or USB-2001-TC for example), it must
                            have an A/D converter with an attached EXP
                            board.  Thermocouples must be wired to EXP
                            channels selected.
"""
from __future__ import absolute_import, division, print_function
from builtins import *  # @UnusedWildImport

import tkinter as tk
import datetime # for logging purposes
import time
import numpy
import os


from lookup_pt100pt1000 import interp_resist_to_temp_np100
from lookup_pt100pt1000 import interp_resist_to_temp_np1000
from mcculw import ul
from mcculw.enums import TempScale, ErrorCode
from mcculw.ul import ULError
from mcculw.device_info import DaqDeviceInfo

try:
    from ui_examples_util import UIExample, show_ul_error
except ImportError:
    from .ui_examples_util import UIExample, show_ul_error


class ULTI02(UIExample):
    def __init__(self, master):
        super(ULTI02, self).__init__(master)
        # By default, the example detects all available devices and selects the
        # first device listed.
        # If use_device_detection is set to False, the board_num property needs
        # to match the desired board number configured with Instacal.
        # BOARD NUMBER IS DEFINED IN TKINTER AT START OF TEST
        use_device_detection = False
        self.running = False
        # Device Detection not used in this test
        try:
            if use_device_detection:
                self.configure_first_detected_device()

            self.device_info = DaqDeviceInfo(self.board_num)
            self.ai_info = self.device_info.get_ai_info()
            if self.ai_info.temp_supported:
                self.create_widgets()
            else:
                self.create_unsupported_widgets()
        except ULError:
            self.create_unsupported_widgets(True)
    # Main update loop that gets repeated every 100ms while the test is running
    def update_values(self):
        try:
            # Get the values from the device (optional parameters omitted)
            # Temp scale set to NOSCALE and conversion will be done via lookup table within this program
            err_code, data_array = ul.t_in_scan(self.board_num, self.low_chan,
                                                self.high_chan, TempScale.NOSCALE)
            # create array of temperature and resistances to be logged, data_array is raw resistance 
            data_example = ""
            data_example_temps = ""
            data_temp_display = numpy.array(data_array)
            data_array = numpy.around(data_array,3)
            for x in range(0,8):
                data_example+=str(data_array[x]) + ';'
                data_example_temps+=str(numpy.around(interp_resist_to_temp_np1000(data_array[x]),2)) + ';'

            # Check err_code for OUTOFRANGE or OPENCONNECTION. All other
            # error codes will raise a ULError and are checked by the except
            # clause.
            # if err_code == ErrorCode.OUTOFRANGE:
            #     self.warning_label["text"] = (
            #         "A thermocouple input is out of range.")
            # elif err_code == ErrorCode.OPENCONNECTION:
            #     self.warning_label["text"] = (
            #         "A thermocouple input has an open connection.")
            # else:
            #     self.warning_label["text"] = ""
            
            # self.display_values(data_array)
            
            # creates variables for time format in log
            current_date_and_time = datetime.datetime.now()
            current_date_and_time_string = current_date_and_time.strftime("%Y-%m-%d %H:%M:%S")
            
            current_time = time.time()
            
            # start_logging Boolean is used to only log at 00 or 30 seconds of the minute
            # this is to have synched timings between two programs running independantly on the same machine
            sub_time = current_time - self.start_time
            seconds = datetime.datetime.now().strftime("%S")
            if seconds == '30' or seconds == '00':
                start_logging = True
            else:
                start_logging = False
            # Log at 00 or 30 seconds every minute (twice a minute)
            if sub_time >=10 and start_logging:
                self.start_time = time.time()
                self.last_logged_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # create log of temperature for the specified time
                try:
                    with open(self.filefullname, "a") as myfile:
                        myfile.write(current_date_and_time_string + ';')
                        myfile.write(data_example_temps + data_example + '\n')
                    myfile.close()
                except:
                    pass
            # Call this method again until the stop button is pressed (or an
            # error occurs)



            # This is the display in the command prompt
            message_timing = current_time - self.start_time_timing
            if message_timing <= 1 and self.verify == 1:
                os.system('cls')
                print('Test Running')
                print('Test Name =', self.test_name)
                print('Last logged data:', self.last_logged_time)
                for x in range(0, 7):
                    print('Channel', x, 'T=', round(interp_resist_to_temp_np1000(data_temp_display[x]),2), '°C')
                self.verify = 2
            elif message_timing >=1 and message_timing <=2 and self.verify == 2:
                os.system('cls')
                print('Test Running.')
                print('Test Name =', self.test_name)
                print('Last logged data:', self.last_logged_time)
                for x in range(0, 7):
                    print('Channel', x, 'T=', round(interp_resist_to_temp_np1000(data_temp_display[x]),2), '°C')
                self.verify = 3
            elif message_timing >=2 and message_timing <=3 and self.verify == 3:
                os.system('cls')
                print('Test Running..')
                print('Test Name =', self.test_name)
                print('Last logged data:', self.last_logged_time)
                for x in range(0, 7):
                    print('Channel', x, 'T=', round(interp_resist_to_temp_np1000(data_temp_display[x]),2), '°C')
                self.verify = 4
            elif message_timing >=3 and message_timing <=4 and self.verify == 4:
                os.system('cls')
                print('Test Running...')
                print('Test Name =', self.test_name)
                print('Last logged data:', self.last_logged_time)
                for x in range(0, 8):
                    print('Channel', x, 'T=', round(interp_resist_to_temp_np1000(data_temp_display[x]),2), '°C')
                self.verify = 5
            elif message_timing > 4 and self.verify == 5:
                self.start_time_timing = time.time()
                self.verify = 1
            else:
                pass

            # self-updating graph for easy visualisation

            



            # keep running after 100 ms if self.running is True
            if self.running:
                self.after(100, self.update_values)
        except ULError as e:
            self.stop()
            show_ul_error(e)


    def display_values(self, array):
        low_chan = self.low_chan
        high_chan = self.high_chan

        for chan_num in range(low_chan, high_chan + 1):
            index = chan_num - low_chan
            self.data_labels[index]["text"] = '{:.3f}'.format(
                array[index]) + "\n"

    def stop(self):
        self.running = False
        self.start_button["command"] = self.start
        self.start_button["text"] = "Start"
        self.low_channel_entry["state"] = tk.NORMAL
        self.high_channel_entry["state"] = tk.NORMAL

    def start(self):
        os.system('cls')
        self.running = True
        self.start_button["command"] = self.stop
        self.start_button["text"] = "Stop"
        self.low_channel_entry["state"] = tk.DISABLED
        self.high_channel_entry["state"] = tk.DISABLED
        self.test_name_entry["state"] = tk.DISABLED
        self.board_number_entry["state"] = tk.DISABLED
        self.low_chan = self.get_low_channel_num()
        self.high_chan = self.get_high_channel_num()
        self.test_name = self.get_test_name()
        self.board_num = self.get_board_num()
        # self.recreate_data_frame()
        self.start_time = time.time()
        self.start_time_timing = time.time()
        self.last_logged_time = 'Nothing logged yet'
        self.verify = 1
        self.inc = 0
        self.create_log_file()
        self.update_values()

        
        
    def create_log_file(self):
        # creates log_file when starting program
        if not os.path.exists('logs'):
            os.makedirs('logs')
        current_date_and_time = datetime.datetime.now()
        current_date_and_time_filename = current_date_and_time.strftime("%Y_%m_%d-%H%M%S") + '_'
        dir = 'logs\\'
        filename = current_date_and_time_filename
        filemission = self.test_name
        file_ext = '.txt'
        self.filefullname = dir + filename + filemission + file_ext
        file = open(self.filefullname, 'a')
        

    def get_low_channel_num(self):
        try:
            return int(self.low_channel_entry.get())
        except ValueError:
            return 0

    def get_high_channel_num(self):
        try:
            return int(self.high_channel_entry.get())
        except ValueError:
            return 0

    def get_test_name(self):
        try:
            return self.test_name_entry.get("1.0",'end-1c')
        except ValueError:
            return 0

    def get_board_num(self):
        try:
            return int(self.board_number_entry.get())
        except ValueError:
            return 0


    def validate_channel_entry(self, p):
        if p == '':
            return True
        try:
            value = int(p)
            if value < 0 or value > self.ai_info.num_temp_chans -1:
                return False
        except ValueError:
            return False

        return True

    def recreate_data_frame(self):
        low_chan = self.low_chan
        high_chan = self.high_chan
        channels_per_row = 4

        new_data_frame = tk.Frame(self.results_group)

        self.data_labels = []
        row = 0
        column = 0
        # Add the labels for each channel
        for chan_num in range(low_chan, high_chan + 1):
            chan_label = tk.Label(new_data_frame, justify=tk.LEFT, padx=3)
            chan_label["text"] = "Channel " + str(chan_num)
            chan_label.grid(row=row, column=column)

            data_label = tk.Label(new_data_frame, justify=tk.LEFT, padx=3)
            data_label.grid(row=row + 1, column=column)
            self.data_labels.append(data_label)

            column += 1
            if column >= channels_per_row:
                row += 2
                column = 0

        self.data_frame.destroy()
        self.data_frame = new_data_frame
        self.data_frame.pack(side=tk.TOP)

    def create_widgets(self):
        '''Create the tkinter UI'''
        self.device_label = tk.Label(self)
        self.device_label.pack(fill=tk.NONE, anchor=tk.NW)
        self.device_label["text"] = ('Board Number ' + str(self.board_num)
                                     + ": " + self.device_info.product_name
                                     + " (" + self.device_info.unique_id + ")")

        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.X, anchor=tk.NW)
        channel_vcmd = self.register(self.validate_channel_entry)

        curr_row = 0

        if self.ai_info.num_temp_chans > 1:

            # Defining low channel entry

            low_channel_entry_label = tk.Label(main_frame)
            low_channel_entry_label["text"] = "Low Channel Number:"
            low_channel_entry_label.grid(
                row=curr_row, column=0, sticky=tk.W)

            self.low_channel_entry = tk.Spinbox(
                main_frame, from_=0,
                to=max(self.ai_info.num_temp_chans - 1, 0),
                validate='key', validatecommand=(channel_vcmd, '%P'))
            self.low_channel_entry.grid(
                row=curr_row, column=1, sticky=tk.W)

            # Defining high channel entry

            curr_row += 1
            high_channel_entry_label = tk.Label(main_frame)
            high_channel_entry_label["text"] = "High Channel Number:"
            high_channel_entry_label.grid(
                row=curr_row, column=0, sticky=tk.W)

            self.high_channel_entry = tk.Spinbox(
                main_frame, from_=0,
                to=max(self.ai_info.num_temp_chans - 1, 0),
                validate='key', validatecommand=(channel_vcmd, '%P'))
            self.high_channel_entry.grid(
                row=curr_row, column=1, sticky=tk.W)

            # Defining test name entry

            curr_row += 1
            test_name_entry_label = tk.Label(main_frame)
            test_name_entry_label["text"] = "Test Name"
            test_name_entry_label.grid(
                row=curr_row, column=0, sticky=tk.W)            

            self.test_name_entry = tk.Text(main_frame, height=1, width=30)
            self.test_name_entry.grid(
                row=curr_row, column=1, sticky=tk.W)

            # Defining board number entry

            curr_row += 1
            board_number_entry_label = tk.Label(main_frame)
            board_number_entry_label["text"] = "Board number:"
            board_number_entry_label.grid(
                row=curr_row, column=0, sticky=tk.W)

            self.board_number_entry = tk.Spinbox(
                main_frame, from_=0,
                to=4,
                validate='key', validatecommand=(channel_vcmd, '%P'))
            self.board_number_entry.grid(
                row=curr_row, column=1, sticky=tk.W)

            # Default Values

            initial_value = min(self.ai_info.num_temp_chans - 1, 7)
            self.high_channel_entry.delete(0, tk.END)
            self.high_channel_entry.insert(0, str(initial_value))

        # self.results_group = tk.LabelFrame(self, text="Results")
        # self.results_group.pack(fill=tk.X, anchor=tk.NW, padx=3, pady=3)

        # self.data_frame = tk.Frame(self.results_group)
        # self.data_frame.pack(side=tk.TOP)

        # self.warning_label = tk.Label(self.results_group, fg="red")
        # self.warning_label.pack(side=tk.BOTTOM)

        button_frame = tk.Frame(self)
        button_frame.pack(fill=tk.X, side=tk.RIGHT, anchor=tk.SE)

        button_frame = tk.Frame(self)
        button_frame.pack(fill=tk.X, side=tk.RIGHT, anchor=tk.SE)

        self.start_button = tk.Button(button_frame)
        self.start_button["text"] = "Start"
        self.start_button["command"] = self.start
        self.start_button.grid(row=0, column=0, padx=3, pady=3)

        quit_button = tk.Button(button_frame)
        quit_button["text"] = "Quit"
        quit_button["command"] = self.master.destroy
        quit_button.grid(row=0, column=1, padx=3, pady=3)

# Start program
def main():
    ULTI02(master=tk.Tk()).mainloop()
main()
