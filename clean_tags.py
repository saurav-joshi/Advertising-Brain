import sys
import re
import itertools
import logging
import os

logger = logging.getLogger('apscheduler.executors.default')
hdlr = logging.FileHandler(os.path.join(os.path.curdir,'logs','myapp.log'))
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

FLAGS = re.MULTILINE | re.DOTALL
slang_words = ["nswf","LMFAOO","Wow","Woow","Wooow","Aww","haha","hahaha","AFAIC","AFAIK","AFAIR","AFK","ASAP","BBL","BBS","BFD","BRB","BTW","B2B","C&V","C|N>K","cya","CU","CYS","FAQ","FFS","FOAF","FYI","G2G","GAGF","GFY","GG","GJ","HAND","HTH","IANAL","IANARS","IC","ICYDK","ICYDN","ICUDK","IIRC","IMHO","IMO","IMNSHO","IRC","IRL","ISTR","IYDMMA","Joo","JOOC","k","l8","l8r","LIEK","LMAO","LOL","MYOB","NM","NOYB","NP","NSFW","NT","O","OIC","OMG","OMFG","OMFL","OOC","OT","OTOH","PFO","PITA","PO","prog","prolly","plz","Pwn","P2P","qoolz","R","RL","ROFL","ROTFL","ROFLMAO","ROTFLMAO","r0x0rz","RTFA","RTFM","RU","R8","SFW","STFU","sux0rs","TBH","thx","TTFN","TIA","TTYL","U","ur","w/e","w/o","WDUWTA","WTF","YMMV","w00t","w8","XO","XOX","XOXO","XOXOXO","XX","XXX","ABT","ABT2","ACDNT","ACK","ACPT","ADD","ADDY","AEAP","AF","AFK","AIGHT","AKA","AMAP","AML","AMOF","ASAP","ATB","ATEOTD","AYT","B2W","B4","BDAY","BF","BF","BF4L","BFF","BLNT","BM","BOYF","BRB","BTW","BYOB","CIAO","CM","CMB","CMON","CR8","CTC","CU","CUA","CUL","CUL8R","CYA","CYAL8R","DOS","DIY","DKDC","D/L","DL","DNT","EMA","EOM","ETA","EZ","EZY","FAQ","FBM","FC","FTW","FW","FWIW","FWM","FYEO","FYA","FYI","G2CU","G2G","G2R","GB","GBTW","GBU","GF","GG","GJ","GL","GMTA","GN","GNIGHT","GNITE","GR8","GRATZ","GTG","GUD","GUDNYT","H8","HAK","HAU","HAV","H&K","H2CUS","HAND","H-BDAY","HF","HFAC","HRU","HTH","HUB","HUYA","HV","HW","IB","IC","IDC","IHNI","IK","ILU","ILY","IM","IMHO","IMO","IMS","IMU","IRL","IUSS","JAC","JK","JLMK","K","KK","KEWL","KIT","KUTGW","L8R","LOL","LOL","LTNS","LUVYA","MC","MOS","MIRL","MKAY","MSG","MTF","MUSM","MWAH","MYOB","N1","N2M","NBD","NE","NE1","NIMBY","NM","NM","NOYB","NP","NT","NVM","NVR","NW","OB","OB","OI","OIC","OJ","OM","OMDB","OMG","OMW","ONL","OTB","OTL","OTOH","OVA","P2P","PEEPS","PIC","PL8","PLMK","PLS","PLZ","PM","POS","POV","PPL","PROLLY","PRT","PZ","QIK","QL","QT","QTPI","RIP","RLY","RME","ROFLOL","RU","RUOK","RX","SBT","SC","SIT","SK8","SK8NG","SK8R","SK8RBOI","SO","SOAB","SOL","SOS","SRSLY","SRY","SS","STR8","SUL","SUP","SUX","SYL","SYS","TBC","TBD","TBL","TC","TGIF","THX","THNX","TMB","TMI","TMTH","TOJ","TTFN","TTLY","TTUL","TU","TTYL","TTYS","TY","UFB","UFN","UL","U-L","UOK","UR","URW","UW","VBS","VIP","VM","VN","VRY","W@","W/","W8","WAH","WAM","WAYF","W/B","WB","WBU","WC","W/E","W/END","WE","WIU","WK","WKD","W/O","WRK","WRU@","WTF","WTG","WTH","WTM","WU","WUF","WUP","X","XME","XOXOXO","XLNT","Y?","Y2K","YARLY","YBS","YGG","YNK","YR","YR","YW","ZUP","ZZZZ"]
slang_words = [slang.lower() for slang in slang_words]

def hashtag(text):
    text = text.group()
    hashtag_body = text[1:]
    if hashtag_body.isupper():
        result = "<hashtag> {} <allcaps>".format(hashtag_body)
    else:
        result = " ".join(["<hashtag>"] + re.split(r"(?=[A-Z])", hashtag_body, flags=FLAGS))
    return result

def allcaps(text):
    text = text.group()
    return text.lower() + " <allcaps>"

def clean(text):
    try:
        # Different regex parts for smiley faces
        eyes = r"[8:=;]"
        nose = r"['`\-]?"

        # function so code less repetitive
        def re_sub(pattern, repl):

            return re.sub(pattern, repl, text, flags=FLAGS)

        text = re_sub(r"https?:\/\/\S+\b|www\.(\w+\.)+\S*", "")
        text = re_sub(r"http[s]*:\/\/", "")
        text = re_sub(r"@\w+[:]*[\s]*['s]*", "")
        #text = re_sub(r"@\w+:", "")
        text = re_sub(r"{}{}[)dD3]+|[)dD3]+{}{}".format(eyes, nose, nose, eyes), "")
        text = re_sub(r"{}{}p+".format(eyes, nose), "")
        text = re_sub(r"{}{}\(+|\)+{}{}".format(eyes, nose, nose, eyes), "")
        text = re_sub(r"{}{}[\/|l*]".format(eyes, nose), "")
        text = re_sub(r"<3","")
        text = re_sub(r"\b[-+/]?[.\d]*[\d]+[:,.\d]*\b", "")
        text = re_sub(r"#\S+", hashtag)
        text = re_sub(r"([!?.]){2,}"," ")
        #text = re_sub(r"\b(\S*?)(.)\2{2,}\b", "\1\2<elong>")
        text = re_sub(r"\bRT\b", "")
        text = re_sub(r"\brt\b", "")
        text = re_sub(r"/"," / ")


        text = ''.join(''.join(s)[:2] for _, s in itertools.groupby(text))
        text = ' '.join([t.strip() for t in text.split(" ") if t.lower() not in slang_words])
        return text.strip()

    except Exception as e:
        return ''
        logger.debug(e.message)
        logger.debug('Error on line {} in file {}'.format(sys.exc_info()[-1].tb_lineno,sys.exc_info()[-1].tb_frame.f_code.co_filename))



if __name__ == '__main__':
    text = "I TEST alllll kinds of #ipl and #HASHTAGS, @mentions and 3000 (http://t.co/dkfjkdf). w/ <3 :) haha!!!!!"
    tokens = clean(text)
