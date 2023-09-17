import os, socket, logging

class AnimdlDaemonJob:
    def __init__(self, daemon, command):
        self.raw_command = command
        self.daemon = daemon
        self.command_list = []

    def __str__(self):
        return str(type(self)) + str(self.command_list)

    def parse(self):
        self.command_list = self.raw_command.split(' ')
        job = AnimdlDaemonJobEmpty(self)
        if len(self.command_list) > 0: 
            command = self.command_list[0]
            if command == "DOWNLOAD":
                job = AnimdlDaemonJobDownload(self)

            elif command == "STREAM":
                job = AnimdlDaemonJobStream(self)

        return job
    
    def execute(self):
        pass

class AnimdlDaemonJobEmpty(AnimdlDaemonJob):
    def __init__(self, daemon_job):
        self.daemon_job = daemon_job
        self.command_list = self.daemon_job.command_list 

    def __str__(self):
        return super().__str__()

    def parse(self, raw_command):
        return None

    def execute(self):
        pass


class AnimdlDaemonJobDownload(AnimdlDaemonJob):
    def __init__(self, daemon_job):
        self.daemon_job = daemon_job
        self.command_list = self.daemon_job.command_list

    def __str__(self):
        return super().__str__()

    def parse(self, raw_command):
        return None

    def execute(self):
        return None

class AnimdlDaemonJobStream(AnimdlDaemonJob):
    def __init__(self, daemon_job):
        self.daemon_job = daemon_job
        self.command_list = self.daemon_job.command_list

    def __str__(self):
        return super().__str__()

    def parse(self, raw_command):
        return None

    def execute(self):
        return None

class AnimdlDaemon:
    def __init__(self, socket_path):
        self.socket_path = socket_path
        try:
            os.unlink(socket_path)
        except OSError:
            if os.path.exists(socket_path):
                raise
        self.server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.server.bind(socket_path)
        self.recieve_buffer_size = 1024
        self.recieve_handlers = []
        self.connection = None
        logging.basicConfig(level=logging.INFO)

    def __del__(self):
        if self.connection:
            self.connection.close()
        os.unlink(self.socket_path)

    def serve(self):
        self.server.listen(1)
        logging.info('Server is listening for jobs...')
        self.connection, client_fd = self.server.accept()
        while True:
            data = self.connection.recv(self.recieve_buffer_size)
            if not data:
                break
            else:
                animdl_job = AnimdlDaemonJob(self, data.decode()).parse()
                logging.info(f'Recieved job \"{animdl_job}\"')
                for recieve_handler in self.recieve_handlers:
                    recieve_handler(animdl_job)

if __name__ == "__main__":
    daemon = AnimdlDaemon('/tmp/animdl-daemon.sock')
    daemon.serve()
