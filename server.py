import socket
import numpy as np
import wavGen
import os
import time

TCP_IP = '127.0.0.1'
TCP_PORT = 44444
BUFFER_SIZE = 20  # Normally 1024, but we want fast response

def sendACK():
    conn.sendall("OK")

def sendFile(filename):
    sendACK()
    size = str(os.stat(filename).st_size)
    sendFileString = "send_file," + filename + "," + size
    print sendFileString
    conn.sendall(sendFileString)
    f = open(filename,'rb')
    print 'Sending...'
    l = f.read(BUFFER_SIZE)
    while (l):
        # print 'Sending...'
        conn.send(l)
        l = f.read(BUFFER_SIZE)
    f.close()
    os.remove(filename)
    print "Done Sending"
    # print conn.recv(1024)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

while 1:
    conn, addr = s.accept()
    print 'Connection address:', addr
    while 1:
        data = conn.recv(BUFFER_SIZE)
        if not data: break
        mystring = data.split(",")
        cmd = mystring[0]

        if (cmd == "send_file"):
            """
            Anounce to the bouy that a file is going to be send
            #send_file,name,size: the send_file message(name of the file, size of the file in bytes)
            """
            print cmd

        elif (cmd == "get_file"):
            """
            #get_file,name,delete: the get_file message requires a file to the node (name of the file required, delete flag, if 1 erase it after sending, otherwise if 0 not). The node answer with OK, then with the send_file command before sending the file.
            """
            print cmd

            filename = mystring[1]+'.wav'
            wavGen.wavGen(filename,"rand")
            sendFile(filename)


        elif (cmd == "get_data"):
            """
            get_data,delete: the get_data message: get whatever data has been recorded. (delete flag, if 1 erase it after sending, if 0 not ).
            Before each file the node sends the corresponding send_file command.
            """
            for value in np.random.uniform(1,12):
                value = int(np.ceil(np.random.uniform(1,100)))
                filename = str(value) +'.wav'
                print filename
                if (value % 17 == 0):
                    wavGen.wavGen(filename,"sine")
                else:
                    wavGen.wavGen(filename,"rand")
                sendFile(filename)

        elif (cmd == "set_power"):
            """
            #set_power,cum_id,s_l: the set_power message(cum_id cumulative list (NOTE1) of the projector IDs where to play the file, s_l source level output power)
            """
            print cmd
            sendACK()

        elif (cmd == "play_audio"):
            """
            # play_audio,name,cum_id,starting_time,n_rip: the play_audio message (name of the file that has to be played, cum_id cumulative list (NOTE1) of the projector IDs where to play the file, starting_time HH:MM:SS when to start playing the file, n_rip number of time it has to be consecutively played, delete flag, if 1 erase it after playing, if 0 not, force_flag if trying to transmit while recording:
            #     0 (default) not allowed (error feedback)
            #     1 (force) stop recording and start transmitting
            #     2 (both) do both the operations together
            # )
            """
            print cmd
            sendACK()

        elif (cmd == "record_data"):
            """
            # record_data,name,sens_t,cum_id,starting_time,duration,force_flag: the record_data message (name of the file where to record the audio, sens_t of the sensors that have to record the data:
            #     1 --> hydrophone,
            #     2 --> camera
            #     3 --> others,
            # cum_id cumulative (NOTE1) list of the sensors IDs used to record the audio, starting_time HH:MM:SS when to start recording the file, duration HH:MM:SS of duration of the recording, force_flag if trying to record while transmitting:
            #     0 (default) not allowed (error feedback)
            #     1 (force) stop transmitting and start recording
            #     2 (both) do both the operations together
            # )
            """
            print cmd
            sendACK()

        elif (cmd == "get_rt_data"):
            """
            #     get_rt_data[0],sens_t[1],cum_id[2],starting_time[3],duration[4],chunck_duration[5],delete[6]:
            the get_rt_data message ask the node to record and send the data in real time, divided them in chunck of fixed time length.
            The node before to send each chunck, sends an IDENTIFIER (e.g. UNIX EPOCH). (cum_id cumulative list of the senseors IDs used to record the audio, sens_t of the sensors that have to record the data:
            #         1 --> hydrophone,
            #         2 --> camera
            #         3 --> others,
            # starting_time HH:MM:SS when to start recording the file, duration HH:MM:SS of duration of the recording, chunck_duration chunk duration [seconds], delete flag, if 1 erase it after sending, otherwise if 0 not, force_flag if trying to record while transmitting:
            #             0 (default) not allowed (error feedback)
            #             1 (force) stop transmitting and start recording
            #             2 (both) do both the operations together
            """
            print "cmd"
            print cmd
            data = data + conn.recv(BUFFER_SIZE)
            if not data: break
            mystring = data.split(",")
            print mystring
            if (mystring[1] == '1'):
                # hydrophone
                cum_id = "{0:80b}".format(int(mystring[2]))
                print cum_id.ljust(8,'0')
                for chunk in range(int(mystring[4])):
                    value = int(time.time())
                    filename = str(value) +'.wav'
                    print filename
                    if (value % 17 == 0):
                        wavGen.wavGen(filename,"sine")
                    else:
                        wavGen.wavGen(filename,"rand")
                    sendFile(filename)
            else:
                sendACK()
        elif (cmd == "get_status"):
            """
            # get_status the get_status message to obtain the node status.
            """
            print cmd
            sendACK()

        elif (cmd == "reset_proj"):
            """
            # reset_proj,cum_id,force_flag: the reset_proj message. This message will reset the projectors (cum_id cumulative (NOTE1) list of the projector IDs that has to be resetted, force_flag if 1 reset also if pending operations, if 0 not )
            """
            print cmd
            sendACK()

        elif (cmd == "reset_sen"):
            """
            # reset_sen,sens_t,cum_id,force_flag: the reset_sen message. This message will reset the sensors(sens_t of the sensors that have to record the data:
            #                 1 --> hydrophone,
            #                 2 --> camera
            #                 3 --> others,
            #         cum_id cumulative list of the projector IDs that has to be resetted, force_flag if 1 reset also if pending operations, if 0 not)
            """
            print cmd
            sendACK()

        elif (cmd == "reset_all"):
            """
            # reset_all,force_flag: the reset_all message. This message will reset the node (force_flag if 1 reset also if pending operations, if 0 not)
            """
            print cmd
            sendACK()

        elif (cmd == "delete_all_rec"):
            """
            # delete_all_rec,sens_t: the delete_all_rec message. This message delete the recorded (sens_t of the sensors that have to record the data:
            #                 o --> all,
            #                 1 --> hydrophone,
            #                 2 --> camera
            #                 3 --> others)
            """
            print cmd
            sendACK()

        elif (cmd == "delete_all_sent"):
            """
            # delete_all_sent: the delete_all_rec message. This message delete the files sent to the node
            """
            print cmd
            sendACK()
        elif (cmd == "run_script"):
            """
            # Run a script
            """
            print cmd
            data = data + conn.recv(BUFFER_SIZE)
            if not data: break
            mystring = data.split(",")
            print mystring
            sendACK()
        else:
            '''
            # report error and proceed
            '''
            print "unknown command : " +', '.join(mystring)



#     conn.send("ok")  # echo
# conn.close()
