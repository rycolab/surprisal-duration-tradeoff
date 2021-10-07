# pylint: disable=global-statement
import torch


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

PAUSE_PHONES = {
    'SIL', '<oov>', 'pau', 'ssil',
}

def read_punct(punct_file):
    punct = set()
    with open(punct_file, 'r') as f:
        for line in f:
            punct |= set([line.strip()])

    return punct


def add_extra_pauses(pauses):
    global PAUSE_PHONES
    PAUSE_PHONES |= pauses


def add_punct(punct_file):
    punct = read_punct(punct_file)
    add_extra_pauses(punct)


REMOVE_CHARS = {
    'epitran': [
        '."', '"', '‘', '—', ',', '’', '!',
        '(', ')', '?', '”', '\'', '“', ';',
        ':', '„', '¿', '¡', '\xad', '»', '«',
        '~', '।', '‹', '›', '৷', '፤', '።', '፦',
        '\x90', '\uea7b', '\x81', '\uea01', '`',
        '_', '\x8d', '\x94', '‑', '\u200c', '\x81',
        '\u200d'
    ]
}
REMOVE_CHARS_LANG = {
    'epitran': {
        'LAOUBS': ['.'],
        'SWESFV': ['.'],
        'TGKIBT': ['.'],
        'MARWTC': ['.'],
    },
}

SPLIT_CHARS = {
    'epitran': [
        '–', '-', '.'
    ],
}

REMOVE_WORDS = {
    'unitran': [
        '(', ')', '’', '”', '―¿', '―', '“', ':-', '“¿', '»”', '»', '«', '‘',
        '—', '—-', '›', '–', '!›', ':*', '/', '”»', '.’', '¿', '.”', '~', '‹',
        ',/', '“/', '?”', '!»', '-/', ').”', '),’', '’”', '—¡', '.»', '//', '“‘',
        '‹‹', '„', '+', '¡', '/(/', '!”', ').›', '–¿', '?»', '=', '--#', 'ʼ', '}',
        '½', '...»', '*', '‚', ')”', '.-', '.–', '°', '‟', '¿«', '››', '«~', ',).’'
        ',”', '#', '’’', '.›', '，', '¼', '；', '«„', ').~»', '~).~»',
        ',).’', ',”', '/–', '.).”', '.).’', '。', '“¡', 'Ξ', '‐', '…', '—“', '：',
        '！', '？', '、', u'\u200f~', '\x8d', u'\u200c',
    ],
}
REMOVE_WORDS_LANG = {
    'unitran': {
        'GUQLPY': ['Ã'],
        'MPGABT': ['Á'],
        'MCPWBT': ['Á'],
        'VIEVOV': ['Ý'],
        'MQBWBT': ['Ì'],
        'URDWTC': ['b'],
        'QVSTBL': ['Z'],
        'CAPSBB': ['–¿Ä'],
        'BIMWBT': ['q'],
        'PORARA': ['Ó'],
        'PORARC': ['Ó'],
        'PORBSP': ['Ó'],
        'BNGBBS': ['৩'],
        'APDAS2': ['٣'],
        'OKUWYI': ['È'],
        'BTDLAI': ['q'],
        'BTTPDT': ['û'],
        'SMLTBL': ['Ā'],
        'BUDIBS': ['Ḿ'],
        'GEJBS2': ['í', 'Ì'],
        'NOTTBL': ['Z'],
        'BKVWYI': ['Ō'],
        'HNSWBT': ['Z'],
        'MZMWBT': ['À'],
        'BNGCLV': ['৩'],
        'BNGWTC': ['৩'],
        'ATGWYI': ['è', 'Ā', 'Ú', 'É'],
        'TBZBSB': ['Ì'],
        'PUISMV': ['X'],
        'HNEBGC': ['६५']
    },
}


LANGUAGES_EPITRAN = [
    'AZEBSA', 'BNGWTC', 'HAUCLV', 'INZNTV', 'JAVNRF', 'LAOUBS', 'RONBSR',
    'SPNBDA', 'SPNR95', 'SWESFV', 'TGKIBT', 'TIRUBS', 'TRKWTC', 'BNGBBS',
    'CEBRPV', 'HNDSKV', 'INZSHL', 'KAZKAZ', 'MARWTC', 'RUSS76', 'SPNDHH',
    'SPNWTC', 'TCVWTC', 'TGLPBS', 'TPIPNG', 'VIEVOV', 'BNGCLV', 'HAEBSE',
    'ILORPV', 'INZTSI', 'KMRUBS', 'POLNCV', 'SOMSIM', 'SPNNVI', 'SWESFB',
    'TCWWTC', 'THATSV', 'TRKBST', 'ZLMAVB',
]

LANGUAGES_WIKIPRON = [
    'EN1NIV', 'LTNNVV', 'MFEBSM', 'MLGRCV', 'MWWHDV', 'NHXNTV', 'PORARA',
    'PORBSP', 'SRNBSS', 'FINV38', 'MAHWGM', 'MLGEIV', 'MLGRPV', 'NH1NMV',
    'ORYWTC', 'PORARC', 'PORNLH', 'URDWTC',
]

LANGUAGES_UNITRAN = [
    'ACUTBL', 'BAVWBT', 'BUSSIM', 'COKWBT', 'ESENTM', 'GUQLPY', 'INZTSI',
    'KIJPNG', 'LAOUBS', 'MCOTBL', 'MOGLAI', 'NHUWBT', 'PAMPBS', 'QUWHLE',
    'SNNWBT', 'TIKWYI', 'URYAOV', 'ADETBL', 'BBOBSB', 'BWQBSB', 'CONWBT',
    'ESSWYI', 'GURIBS', 'IPIPNG', 'KJBSBG', 'LASABT', 'MCPWBT', 'MOPWBT',
    'NHWTBL', 'PAUUBS', 'QUYSBU', 'SNWWBT', 'TIRUBS', 'VIEVOV', 'ADHBSU',
    'BCLBPV', 'BWUTBL', 'CRHIBT', 'EUSEAB', 'GUXABB', 'IRIWYI', 'KJEWBT',
    'LAWNTM', 'MCQTBL', 'MORBSS', 'NHXNTV', 'PBBWBT', 'QUZPBS', 'SOMSIM',
    'TLBLAI', 'VMWBSM', 'ADJWBT', 'BCWWBT', 'BZHPNG', 'CRNWBT', 'EWEBSG',
    'GVCTBL', 'IRKBST', 'KJHIBT', 'LEEWBT', 'MCUTBL', 'MPGABT', 'NHYTBL',
    'PBCBSS', 'QVCTBL', 'SOYSIM', 'TLJWBT', 'VUNBST', 'AEUWBT', 'BEHWBT',
    'BZJBSW', 'CSKATB', 'EWEIBS', 'GVLABT', 'ITVSTP', 'KKIBST', 'LEFTBL',
    'MDAWBT', 'MPMTBL', 'NIAIBS', 'PBIWYI', 'QVMTBL', 'SPNBDA', 'TMCBIV',
    'WMWWYI', 'AGNWPS', 'BEPLAI', 'CA1WBT', 'CSOTBL', 'FALTBL', 'GWRWBT',
    'IX1WBT', 'KKJWBT', 'LEMWBT', 'MDYBSE', 'MPXPNG', 'NIJLAI', 'PCMTSC',
    'QVNLLB', 'SPNDHH', 'TNATBL', 'XALIBT', 'AGRTBL', 'BEXWBT', 'CAAWBT',
    'CT1TEV', 'FARWBT', 'GYMWBT', 'IXIWBT', 'KLENLI', 'LEWLAI', 'MEJTBL',
    'MQBWBT', 'NIMBST', 'PESTPV', 'QVOVAA', 'SPNNVI', 'TOBBSA', 'XEDWYI',
    'AGUNVS', 'BFABSS', 'CABNVS', 'CTUBSM', 'FIJBSP', 'GYRSBB', 'IXLWBT',
    'KMAWBT', 'LEXWBT', 'MENBSL', 'MQJLAI', 'NINWYI', 'PIRWBT', 'QVSTBL',
    'SPNR95', 'TOCTBL', 'XMMLAI', 'AHKTBS', 'BFDWBT', 'CACSBG', 'CUCTBL',
    'FINV38', 'HAEBSE', 'JACWBT', 'KMHKOV', 'LGGBSU', 'MEQWBT', 'MRWNVS',
    'NKOWBT', 'PISWBT', 'QVWTBL', 'SPNWTC', 'TOHSBM', 'XO2IBS', 'AIAWYI',
    'BFOBSB', 'CAKSBG', 'CUIWBT', 'FIZTBL', 'HAGGIL', 'JAISBG', 'KMRUBS',
    'LHUTBS', 'MF1WBT', 'MSYPNG', 'NLCLAI', 'PKBBTL', 'QVZWBT', 'SPPTBL',
    'TOSTBL', 'XOGBSU', 'AK1BSG', 'BGRBBS', 'CAPSBB', 'CUKNVS', 'FLMUBS',
    'HAKTHV', 'JAMBSW', 'KNETBL', 'LIABSL', 'MFEBSM', 'MUHWBT', 'NMZWSB',
    'PLSWYI', 'QWHLLB', 'SPYWBT', 'TPIPNG', 'XRBWBT', 'AKEBSS', 'BHZLAI',
    'CARBSS', 'CWEPBT', 'FONBSB', 'HATSBH', 'JAVNRF', 'KNFWYI', 'LIPWBT',
    'MFIWYI', 'MUPNLL', 'NNBBSU', 'PLWWBT', 'QXHWBT', 'SRIWBT', 'TPMWBT',
    'XSBWYI', 'AKPWBT', 'BIBWBT', 'CAXSBB', 'CWTATB', 'FRDWBT', 'HAUCLV',
    'JBUIBS', 'KNJSBI', 'LJPLAI', 'MFKABC', 'MURTBL', 'NNWWBT', 'PMFNTM',
    'QXNWBT', 'SRMWBT', 'TPPTBL', 'XSMBFV', 'ALJOMF', 'BIMWBT', 'CBSBSP',
    'CYAAVV', 'FRNPDC', 'HAYBST', 'JICWBT', 'KNKBSL', 'LLNABT', 'MFQABT',
    'MUYWBT', 'NODWBT', 'POEWYI', 'QXRBSE', 'SRNBSS', 'TPTTBL', 'XSMWBT',
    'ALPWBT', 'BISBSP', 'CBTTBL', 'DA1EST', 'FRNPDV', 'HEHBST', 'JIVAIE',
    'KNOBSL', 'LMEABT', 'MFYWBT', 'MVCNVS', 'NOGIBT', 'POHBSG', 'REJLAI',
    'STNBSP', 'TRKBST', 'XSRWBT', 'ALSBSA', 'BIVWBT', 'CBVTBL', 'DA2WST',
    'FUFPBT', 'HIFBSP', 'JMCBST', 'KOGWBT', 'LNDBSM', 'MFZBSS', 'MVJWBT',
    'NOTTBL', 'POHPOC', 'RIMBST', 'SUACLV', 'TRKWTC', 'XSUMEV', 'ALTIBT',
    'BJVWYI', 'CCESBM', 'DAAWYI', 'FUQWBT', 'HIGTBL', 'JUNWIN', 'KPVIBT',
    'LOBBSB', 'MGDBSS', 'MVPLAI', 'NPLWYI', 'POITBL', 'RMORAM', 'SUNIBS',
    'TRSUTI', 'XTDTBL', 'ALZBSU', 'BKVWYI', 'CEBRPV', 'DAHPNG', 'GAGIB1',
    'HILHPV', 'JVNTBL', 'KPZBSU', 'LOKLBT', 'MGOWYI', 'MWVLAI', 'NPYLAI',
    'POLNCV', 'RMYCVV', 'SURIBS', 'TS1BSM', 'XTMTBL', 'AMFSIM', 'BLTEPI',
    'CEGNTP', 'DBQWYI', 'GAGIBT', 'HNDSKV', 'KAAIBT', 'KQETBL', 'LONBSM',
    'MHIBSU', 'MWWHDV', 'NSUWBT', 'PORARA', 'RONBSR', 'SUSPBT', 'TSZBSM',
    'XUOWBT', 'AMKWBT', 'BLZLAI', 'CGCTBL', 'DESWBT', 'GBILAI', 'HNEBGC',
    'KABCEB', 'KQPWBT', 'LSIBSM', 'MHMBSB', 'MXBMVR', 'NTMWBT', 'PORARC',
    'RUGWBT', 'SUZWBT', 'TTCWBT', 'YAZTBL', 'ANNWBT', 'BMQBSM', 'CHEIBT',
    'DGABSG', 'GDEWBT', 'HNNOMF', 'KACUBS', 'KQYBSE', 'LSMBSU', 'MHMCAT',
    'MXTTBL', 'NTRWBT', 'PORBSP', 'RUNBSB', 'SWESFB', 'TTRIBT', 'YCLNVS',
    'ANVWBT', 'BMVCAB', 'CHNUN1', 'DGIABB', 'GEJBS2', 'HNSWBT', 'KAOABM',
    'KRCLIO', 'LTNNVV', 'MHXBSM', 'MYBABT', 'NUJWBT', 'PORNLH', 'RUSS76',
    'SWESFV', 'TU1TBL', 'YUASBM', 'APDAS2', 'BNGBBS', 'CHVIBT', 'DIKTBL',
    'GILBSP', 'HTOWBT', 'KAQTBL', 'KRINVS', 'LUCHLA', 'MHYLAI', 'MYKWBT',
    'NUSBSS', 'PPKLAI', 'SAGCAR', 'SXNLAI', 'TUEWBT', 'YUHSBV', 'APRWBT',
    'BNGCLV', 'CHZWBT', 'DJKWBT', 'GKNIBS', 'HUBWBT', 'KAZKAZ', 'KRJWBT',
    'LWOWBT', 'MIBTBL', 'MYXBSU', 'NWBWBT', 'PRFWBT', 'SASLAI', 'TAJWBT',
    'TUFWYI', 'ZLMAVB', 'ARBIBS', 'BNGWTC', 'CJPTJV', 'DOMBEC', 'GMVTBL',
    'HUIPNG', 'KBPRCV', 'KRUFMP', 'MAASAV', 'MIFWBT', 'MYYWBT', 'NYFBTL',
    'PRSGNN', 'SBANVV', 'TAQWBT', 'TUOWBT', 'ZYPWBT', 'ARZVDV', 'BOATBL',
    'CK1WBT', 'DOPBSB', 'GNGWYI', 'HUSLLB', 'KBRSIM', 'KSBBST', 'MAASJV',
    'MILTBL', 'MZAWBT', 'NYNBSU', 'PSELAI', 'SBDABB', 'TBYLAI', 'TWBOMF',
    'ATGWYI', 'BOJWBT', 'CKIWBT', 'DSHBTL', 'GNWNTM', 'HUUTBL', 'KCGWBT',
    'KTBBSE', 'MADIBS', 'MINLAI', 'MZKTBL', 'NYOBSU', 'PTULAI', 'SBLTBL',
    'TBZBSB', 'TWULAI', 'ATQLAI', 'BOVWBT', 'CKKWBT', 'DTPBSM', 'GO1TBL',
    'HUVTBL', 'KD1BSU', 'KTJWBT', 'MAGSSI', 'MIOWBT', 'MZMWBT', 'NYYBST',
    'PUISMV', 'SDALAI', 'TCATBL', 'TXATBL', 'AVAIBT', 'BOXWYI', 'CKOGIL',
    'DTSABM', 'GOFTBL', 'IBATIV', 'KDCPBT', 'KUBTBL', 'MAHWGM', 'MIQSBN',
    'NANTTV', 'NZIBSG', 'PWWTBS', 'SEHBSM', 'TCCBST', 'TXUTBL', 'AVNWBT',
    'BPRWYI', 'CKWNVS', 'DUGBTL', 'GOGBST', 'ICRWYI', 'KDIBSU', 'KUEPNG',
    'MAIWBT', 'MITTBL', 'NASPNG', 'OBOWBT', 'PXMBSM', 'SEYWBT', 'TCVWTC',
    'TYVIBT', 'AVUWBT', 'BPSWPS', 'CLETBL', 'DWRTBL', 'GORLAI', 'IFAWBT',
    'KDJBSU', 'KUMIBT', 'MAJTBL', 'MIYWYI', 'NCHTBL', 'OJ1CBS', 'QEJLLB',
    'SGBTBL', 'TCWWTC', 'TZBSBM', 'AWAWTC', 'BQCSIM', 'CMEWBT', 'DYIIBS',
    'GQRWBT', 'IFBTBL', 'KDNBSZ', 'KUSTBL', 'MAKLAI', 'MJSWTC', 'NCJTBL',
    'OKUWYI', 'QU1LSM', 'SGWBSE', 'TEMBSL', 'TZCSBM', 'AWBTBL', 'BQJATB',
    'CMOWBT', 'DYOBSG', 'GSOCAR', 'IFEWBT', 'KEKIBS', 'KVNWBT', 'MAMSBG',
    'MLGEIV', 'NCUWBT', 'OLDBST', 'QUBPBS', 'SHIRBD', 'TEOBSU', 'TZESBM',
    'AYMBSB', 'BQPSIM', 'CMRWBT', 'DYUBSB', 'GU1WBT', 'IFKTBL', 'KEKSBG',
    'KWIWBT', 'MARWTC', 'MLGRCV', 'NDZWBT', 'OM1TBL', 'QUCBLA', 'SHKBSS',
    'TERTBL', 'TZHSBM', 'AYMSBU', 'BRUNXB', 'CNHBSM', 'DYUWYI', 'GUBWBT',
    'IFUWPS', 'KENWBT', 'KXCBSE', 'MAWWBT', 'MLGRPV', 'NEBWYI', 'ORYWTC',
    'QUFLLB', 'SHPTBL', 'TFRWBT', 'TZTWBT', 'AZEBSA', 'BSSWBT', 'CNIWBT',
    'EKAWYI', 'GUDBSC', 'IFYWBT', 'KEOBSU', 'KYCPNG', 'MAZTBL', 'MLYBSM',
    'NEWNCL', 'OSSIBT', 'QUHRBV', 'SIGWBT', 'TGKIBT', 'UDMIBT', 'AZGTBL',
    'BTDLAI', 'CNKBSM', 'EMPWYI', 'GUGRPV', 'IGNSBB', 'KERABT', 'KYFWBT',
    'MBBWPS', 'MMSBSG', 'NFRIBS', 'OTETBL', 'QUHSBB', 'SILGIL', 'TGLPBS',
    'UDUSIM', 'AZZTBL', 'BTSLAI', 'CNLTBL', 'EN1NIV', 'GUHWBT', 'ILORPV',
    'KEZLCN', 'KYQWYI', 'MBTWBT', 'MNBTBL', 'NGUTBL', 'OZMTBL', 'QUJPMC',
    'SJATBL', 'TGOTBL', 'UI1UMK', 'BAKIBT', 'BTTPDT', 'CNMRGB', 'ENBBTL',
    'GUISBU', 'INBWBT', 'KHKMUB', 'KYZWBT', 'MCAWYI', 'MNFCAB', 'NH1NMV',
    'PABTBL', 'QULSBB', 'SLDTBL', 'TGPWBT', 'URATBL', 'BAMLSB', 'BTXLAI',
    'CNTTBL', 'ENXBSP', 'GUMTBL', 'INZNTV', 'KIABSC', 'KZFLAI', 'MCBTBL',
    'MNKBSG', 'NHETBL', 'PADTBL', 'QUPTBL', 'SMLTBL', 'THATSV', 'URBWBT',
    'BANIBS', 'BUDIBS', 'COEWBT', 'ERVWTC', 'GUOWBT', 'INZSHL', 'KIAWBT',
    'LAJBSU', 'MCDTBL', 'MOAWBT', 'NHIWBT', 'PAGPBS', 'QUTIBS', 'SMOBSP',
    'THKBTL', 'URDWTC',
]
