import wavGen
import os

def parse(s,*params):
    print "*******"
    print params
    print "*******"
    cmd = params[0][0]
    if (cmd == "send_file"):
        print cmd
        #send_file,name,size: the send_file message(name of the file, size of the file in bytes)
    elif (cmd == "get_file"):
        print cmd
        filename = params[0][1]+'.wav'
        wavGen.wavGen(filename,"rand")
        s.sendall("send_file,name,size," + filename + "," + str(os.stat(filename).st_size))
        f = open(filename,'rb')
        print 'Sending...'
        l = f.read(1024)
        while (l):
            print 'Sending...'
            s.send(l)
            l = f.read(1024)
        f.close()
        print "Done Sending"
        print s.recv(1024)
        #get_file,name,delete: the get_file message requires a file to the node (name of the file required, delete flag, if 1 erase it after sending, otherwise if 0 not). The node answer with OK, then with the send_file command before sending the file.
    elif (cmd == "get_data"):
        print cmd
        #get_data,delete: the get_data message: get whatever data has been recorded. (delete flag, if 1 erase it after sending, if 0 not ). Before each file the node sends the corresponding send_file command.
    elif (cmd == "set_power"):
        print cmd
        #set_power,cum_id,s_l: the set_power message(cum_id cumulative list (NOTE1) of the projector IDs where to play the file, s_l source level output power)
    elif (cmd == "play_audio"):
        print cmd
        # play_audio,name,cum_id,starting_time,n_rip: the play_audio message (name of the file that has to be played, cum_id cumulative list (NOTE1) of the projector IDs where to play the file, starting_time HH:MM:SS when to start playing the file, n_rip number of time it has to be consecutively played, delete flag, if 1 erase it after playing, if 0 not, force_flag if trying to transmit while recording:
        #     0 (default) not allowed (error feedback)
        #     1 (force) stop recording and start transmitting
        #     2 (both) do both the operations together
		# )
    elif (cmd == "record_data"):
        print cmd
        # record_data,name,sens_t,cum_id,starting_time,duration,force_flag: the record_data message (name of the file where to record the audio, sens_t of the sensors that have to record the data:
        #     1 --> hydrophone,
        #     2 --> camera
        #     3 --> others,
        # cum_id cumulative (NOTE1) list of the sensors IDs used to record the audio, starting_time HH:MM:SS when to start recording the file, duration HH:MM:SS of duration of the recording, force_flag if trying to record while transmitting:
        #     0 (default) not allowed (error feedback)
        #     1 (force) stop transmitting and start recording
        #     2 (both) do both the operations together
        # )
    elif (cmd == "get_rt_data"):
        print cmd
    #     get_rt_data,sens_t,cum_id,starting_time,duration,chunck_duration,delete: the get_rt_data message ask the node to record and send the data in real time, divided them in chunck of fixed time length. The node before to send each chunck, sends an IDENTIFIER (e.g. UNIX EPOCH). (cum_id cumulative list of the senseors IDs used to record the audio, sens_t of the sensors that have to record the data:
    #         1 --> hydrophone,
    #         2 --> camera
    #         3 --> others,
    # starting_time HH:MM:SS when to start recording the file, duration HH:MM:SS of duration of the recording, chunck_duration chunk duration [seconds], delete flag, if 1 erase it after sending, otherwise if 0 not, force_flag if trying to record while transmitting:
    #             0 (default) not allowed (error feedback)
    #             1 (force) stop transmitting and start recording
    #             2 (both) do both the operations together
    elif (cmd == "get_status"):
        print cmd
        # get_status the get_status message to obtain the node status.
    elif (cmd == "reset_proj"):
        print cmd
        # reset_proj,cum_id,force_flag: the reset_proj message. This message will reset the projectors (cum_id cumulative (NOTE1) list of the projector IDs that has to be resetted, force_flag if 1 reset also if pending operations, if 0 not )
    elif (cmd == "reset_sen"):
        print cmd
        # reset_sen,sens_t,cum_id,force_flag: the reset_sen message. This message will reset the sensors(sens_t of the sensors that have to record the data:
        #                 1 --> hydrophone,
        #                 2 --> camera
        #                 3 --> others,
        #         cum_id cumulative list of the projector IDs that has to be resetted, force_flag if 1 reset also if pending operations, if 0 not)
    elif (cmd == "reset_all"):
        print cmd
        # reset_all,force_flag: the reset_all message. This message will reset the node (force_flag if 1 reset also if pending operations, if 0 not)
    elif (cmd == "delete_all_rec"):
        print cmd
        # delete_all_rec,sens_t: the delete_all_rec message. This message delete the recorded (sens_t of the sensors that have to record the data:
        #                 o --> all,
        #                 1 --> hydrophone,
        #                 2 --> camera
        #                 3 --> others)
    elif (cmd == "delete_all_sent"):
        print cmd
    else:
        print "unknown command"
        # delete_all_sent: the delete_all_rec message. This message delete the files sent to the node
