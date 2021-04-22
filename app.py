''' license checker tool'''
from plugins.atlassian import CheckAtlassian
from plugins.sonar import CheckSonar

if __name__ == "__main__":
    CheckAtlassian().call()

