from flask import request, jsonify, make_response
import subprocess
import urllib.parse
import threading
import time
import os


class Terminal:
    def __init__(self) -> None:
        self.process = None
        self.output = b''
        self.complete = False

    # This method starts the command execution
    def execute_commands(self, command):
        try: 
            decoded_command = urllib.parse.unquote(command)
            
            # Use shell=True for Windows or if the command is a string
            self.process = subprocess.Popen(decoded_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Start a thread to read the output in the background
            output_thread = threading.Thread(target=self._fetch_output)
            output_thread.start()

            return make_response(jsonify({"status": "Command started"}), 200)

        except Exception as e:
            return make_response(jsonify({"error": f"An error occurred: {str(e)}"}), 500)

    # This method continuously reads output from the process
    def _fetch_output(self):
        while True:
            if self.process is not None:
                # Fetch available output (without blocking)
                output = self.process.stdout.read(1024)  # Fetch 1024 bytes at a time
                if output:
                    self.output += output
                if self.process.poll() is not None:
                    self.complete = True
                    break
            time.sleep(1)

    # This method allows fetching the output in parts
    def get_partial_output(self):
        if self.output:
            # Fetch part of the output and clear the buffer
            output_to_return = self.output.decode('utf-8')
            self.output = b''  # Clear buffer after sending the data
            return output_to_return
        elif self.complete:
            return "Process completed."
        else:
            return "No new output."
