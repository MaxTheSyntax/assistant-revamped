import gui
import logging

logging.basicConfig(level=logging.DEBUG)
# Set loggers from libraries to WARNING level to reduce verbosity
for logger_name in logging.root.manager.loggerDict:
    logging.getLogger(logger_name).setLevel(logging.WARNING)

def main():
    gui.init()

if __name__ == "__main__":
    main()