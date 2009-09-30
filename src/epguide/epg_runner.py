from common import Config
from epguide import EpGuide
import sys

# -l
# -c 1,2,3 -d 2009-09-12 -f xmltv -o tv.xmltv

def RunEpguide():
    """
    glowna petla aplikacji, odczytuje konfiguracje, uruchamia operacje
    """
    config = Config()
    config.ParseCommandLine(sys.argv)
    if config.options.use_config:
        config.ReadConfigFile()

    epguide = EpGuide(config)
    epguide.Execute()

if __name__ == '__main__':
    RunEpguide()
    