
import logging

def get_logger(name):
    #log_format = '%(asctime)s  %(name)8s  %(levelname)5s  %(message)s'
    log_format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s'
    logging.basicConfig(level=logging.DEBUG,
                        format=log_format,
                        filename='dev.log',
                        datefmt='%Y-%m-%d:%H:%M:%S',
                        filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(logging.Formatter(log_format))
    logging.getLogger(name).addHandler(console)
    return logging.getLogger(name)

