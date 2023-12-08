
from time import process_time_ns
from tradingview_ta import TA_Handler, Interval

# Define the list of symbols
psx_symbols = [
"AABS","AAL","AASM","AATM","ABL","ABOT","ABSON","ACPL","ADAMS","ADMM","ADOS","AEL","AGHA","AGIC","AGIL",
"AGL","AGP","AGSML","AGTL","AHCL","AHL","AHTM","AICL","AIRLINK","AKBL","AKDHL","AKDSL","AKGL","ALAC",
"ALIFE","ALNRS","ALTN","AMBL","AMSL","AMTEX","ANL","ANNT","ANSM","ANTM","APL","APOT","ARCTM","ARM","ARPAK","ARPL","ARUJ","ASC","ASHT","ASIC","ASL","ASTL","ASTM","ATBA","ATIL","ATLH","ATRL","AVN","AWTX","AWWAL",
"AZMT","BAFL","BAFS","BAHL","BAPL","BATA","BCL","BECO","BELA","BERG","BFMOD","BGL","BHAT","BIFO","BIIC",
"BILF","BIPL","BNL","BNWM","BOK","BOP","BPL","BRR","BTL","BUXL","BWCL","BWHL","CASH","CCM","CENI","CEPB",
"CFL","CHAS","CHBL","CHCC","CJPL","CLOV","CLVL","CNERGY","COLG","CPHL","CPPL","CRTM","CSAP","CSIL","CTM",
"CWSM","CYAN","DAAG","DADX","DATM","DAWH","DBCI","DBSL","DCL","DCR","DCTL","DEL","DFML","DFSM","DGKC","DIIL",
"DINT","DKTM","DLL","DMTM","DMTX","DNCC","DOL","DOMF","DSFL","DSIL","DSL","DSML","DWAE","DWSM","DWTM",
"DYNO","ECOP","EFERT","EFGH","EFUG","EFUL","ELCM","ELSM","EMCO","ENGL","ENGRO","EPCL","EPCLPS","EPQL","ESBL",
"EWIC","EXIDE","EXTR","FABL","FAEL","FANM","FASM","FATIMA","FCCL","FCEL","FCEPL","FCIBL","FCONM","FCSC","FDIBL","FECM","FECTC",
"FEM","FEROZ","FFBL","FFC","FFL","FFLM","FHAM","FIBLM","FIL","FIM","FIMM","FLYNG","FML","FNBM","FNEL","FPJM",
"FPRM","FRCL","FRSM","FSWL","FTHM","FTMM","FTSM","FUDLM","FZCM","GADT","GAMON","GATI","GATM","GCIL","GEMPAPL","GEMSPNL","GEMUNSL","GFIL","GGGL",
"GGL","GHGL","GHNI","GHNL","GIL","GLAXO","GLOT","GLPL","GOC","GRR","GRYL","GSKCH","GSPM","GTECH","GTYR","GUSM","GUTM","GVGL","GWLC","HABSM",
"HADC","HAEL","HAFL","HAJT","HASCOL","HATM","HBL","HCAR","HCL","HGFA","HICL","HIFA","HINO","HINOON","HIRAT","HKKT","HMB","HMIM","HMM","HRPL","HSPI","HTL","HUBC","HUMNL",
"HUSI","HWQS","IBFL","IBLHL","ICCI","ICI","ICIBL","ICL","IDRT","IDSM","IDYM","IGIHL","IGIL","ILP","IMAGE",
"IML","INDU","INIL","INKL","INMF","ISIL","ISL","ITTEFAQ","JATM","JDMT","JDWS","JGICL","JKSM","JLICL",
"JOPP","JPGL","JSBL","JSCL","JSGCL","JSIL","JSML","JUBS","JVDC","KAKL","KAPCO","KASBM","KCL","KEL","KHTC","KHYT",
"KML","KOHC","KOHE","KOHP","KOHTM","KOIL","KOSM","KPUS","KSBP","KSTM","KTML","LEUL","LMSM","LOADS","LOTCHEM",
"LPGL","LPL","LUCK","MACFL","MACTER","MARI","MCB","MCBAH","MDTL","MEBL","MEHT","MERIT","META","MFFL",
"MFL","MFTM","MIRKS","MLCF","MODAM","MOHE","MQTM","MRNS","MSCL","MSOT","MTL","MUBT","MUGHAL","MUREB","MWMP",
"NAFL","NAGC","NATF","NATM","NBP","NCL","NCML","NCPL","NESTLE","NETSOL","NEXT","NICL","NINA","NMFL","NML",
"NONS","NPL","NRL","NRSL","NSRM","OBOY","OCTOPUS","OGDC","OLPL","OLPM","OML","ORM","OTSU","PABC","PACE",
"PAEL","PAKD","PAKL","PAKMI","PAKOXY","PAKRI","PAKT","PASL","PASM","PCAL","PDGH","PECO","PGLC","PHDL","PIAA",
"PIBTL","PICL","PICT","PIL","PIM","PINL","PIOC","PKGI","PKGP","PKGS","PMI","PMPK","PMRS","PNSC","POL",
"POML","POWER","POWERPS","PPL","PPP","PPVC","PREMA","PRET","PRIB","PRIC","PRL","PRWM","PSEL","PSMC","PSO",
"PSX","PSYL","PTC","PTL","PUDF","QUET","QUICE","QUSW","RCML","REDCO","REGAL","REWM","RICL","RMPL","RPL",
"RUBY","RUPL","SAIF","SANE","SANSM","SAPL","SAPT","SARC","SASML","SAZEW","SBL","SCBPL","SCHT","SCL","SDOT",
"SEARL","SEL","SEPL","SERT","SFAT","SFL","SGABL","SGF","SGPL","SHCI","SHCM","SHDT","SHEL","SHEZ","SHFA",
"SHJS","SHNI","SHSML","SIBL","SICL","SIEM","SILK","SINDM","SITC","SKRS","SLCL","SLL","SLYT","SMBL","SMCPL",
"SML","SNAI","SNBL","SNGP","SPEL","SPL","SPLC","SPWL","SRVI","SSGC","SSIC","SSML","SSOM","STCL","STJT",
"STML","STPL","SUHJ","SURAJ","SURC","SUTM","SYS","SZTM","TAJT","TATM","TCORP","TCORPCPS","TELE","TGL",
"THALL","THCCL","TICL","TOMCL","TOWL","TPL","TPLI","TPLP","TPLT","TREET","TRG","TRIBL","TRIPF","TRSM",
"TSBL","TSMF","TSML","TSPL","UBDL","UBL","UCAPM","UDPL","UNIC","UNITY","UPFL","USMT",
"UVIC","WAHN","WAVES","WHALE","WTL","YOUW","ZAHID","ZELP","ZHCM","ZIL","ZTL"
]
# Sort the psx_symbols list in ascending order
psx_symbols.sort()
# Iterate over each symbol
for symbol in psx_symbols:
    try:
        # Get the summary of the specified stock
        output1M = TA_Handler(symbol=symbol, screener="PAKISTAN", exchange="PSX", interval=Interval.INTERVAL_1_MONTH)
        output1W = TA_Handler(symbol=symbol, screener="PAKISTAN", exchange="PSX", interval=Interval.INTERVAL_1_WEEK)
        output1D = TA_Handler(symbol=symbol, screener="PAKISTAN", exchange="PSX", interval=Interval.INTERVAL_1_DAY)
        
        # Get the summary of the specified stock if output is not None
        if output1M is not None:
            if output1M.get_analysis() is not None:
                summary = output1M.get_analysis().summary
                RSI = output1M.get_analysis().indicators['RSI']
                RSI_Last = output1M.get_analysis().indicators['RSI[1]']
                Close= output1M.get_analysis().indicators['close']
                Volume= output1M.get_analysis().indicators['volume']
                AO = output1M.get_analysis().indicators['AO']
                Time = output1M.get_analysis().time
                # Print the symbol and its summary
                print(f"Technical Analysis Date: {Time}")
                print(f"Symbol: {symbol}")
                print(summary)
                print(f"MONTHLY Close: {Close}")
                print(f"MONTHLY Volume: {Volume}")
                print(f"MONTHLY RSI: {RSI}")
                print(f"LAST MONTHLY RSI: {RSI_Last}")
                print(f"MONTHLY AO: {AO}")
                
                if output1W is not None:
                    if output1W.get_analysis() is not None:
                        summary = output1W.get_analysis().summary
                        RSI = output1W.get_analysis().indicators['RSI']
                        RSI_Last = output1W.get_analysis().indicators['RSI[1]']
                        Close= output1W.get_analysis().indicators['close']
                        AO = output1W.get_analysis().indicators['AO']
                        Volume= output1W.get_analysis().indicators['volume']
                        Time = output1W.get_analysis().time
                        # Print the symbol and its summary
                        print(summary)
                        print(f"WEEKLY Close: {Close}")
                        print(f"WEEKLY Volume: {Volume}")
                        print(f"WEEKLY RSI: {RSI}")
                        print(f"LAST WEEKLY RSI: {RSI_Last}")
                        print(f"WEEKLY AO: {AO}")
      
        print()
    except Exception as e:
        continue
    

